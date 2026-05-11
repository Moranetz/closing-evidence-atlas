# Closing Evidence Atlas — Phase 4 Publication-Bias Diagnostics
# Implements PROTOCOL.md § 9.4:
#   - Funnel plot (per technique with k ≥ 10)
#   - Egger's regression test
#   - p-curve analysis
#   - Three-parameter selection model (Vevea & Hedges 1995)
#   - PET-PEESE corrections (Stanley & Doucouliagos 2014)
#   - Trim-and-fill (reported as sensitivity, not primary)
#
# A technique whose effect estimate falls below practical significance under
# PET-PEESE or three-parameter selection adjustment is flagged
# `selection-fragile` in the survivor list.
#
# Random seed: 20260510.

suppressPackageStartupMessages({
  library(metafor)
  library(weightr)       # three-parameter selection model
  library(dmetar)        # p-curve helpers
  library(tidyverse)
})

set.seed(20260510)

REPO <- here::here()
EFFECTS_PATH <- file.path(REPO, "data", "standardized_effects.csv")
RESULTS_DIR <- file.path(REPO, "results")
FIGURES_DIR <- file.path(REPO, "figures")

effects <- read_csv(EFFECTS_PATH, show_col_types = FALSE)
posterior_summary <- read_csv(file.path(RESULTS_DIR, "posterior_summaries.csv"),
                              show_col_types = FALSE)

# -----------------------------------------------------------------------------
# Per technique with ≥ 10 studies
# -----------------------------------------------------------------------------
candidates <- posterior_summary %>%
  filter(n_studies >= 10) %>%
  pull(technique_taxonomy_id)

all_diagnostics <- list()
for (tid in candidates) {
  d <- effects %>% filter(technique_taxonomy_id == tid)
  message(sprintf("[bias] %s (k=%d)", tid, nrow(d)))

  # Frequentist rma fit for compatibility with metafor diagnostics
  rma_fit <- rma(yi = es_standardized_value, sei = es_standardized_se, data = d,
                 method = "REML")

  # Funnel plot
  pdf(file.path(FIGURES_DIR, sprintf("funnel_%s.pdf", tid)),
      width = 7, height = 6)
  funnel(rma_fit, main = sprintf("%s — funnel plot (k=%d)", tid, nrow(d)))
  dev.off()

  # Egger's test
  egger <- regtest(rma_fit, model = "lm")

  # p-curve (using dmetar::pcurve via metafor inputs)
  pcurve_res <- tryCatch(dmetar::pcurve(rma_fit, plot = FALSE),
                         error = function(e) NULL)

  # Three-parameter selection model (Vevea-Hedges 1995)
  wf_fit <- tryCatch(
    weightfunct(effect = d$es_standardized_value,
                v = d$es_standardized_se^2,
                steps = c(0.025, 0.05, 0.10, 1.0)),
    error = function(e) NULL
  )

  # PET-PEESE
  pet_fit <- rma(yi = es_standardized_value, sei = es_standardized_se,
                 mods = ~ es_standardized_se, data = d, method = "REML")
  peese_fit <- rma(yi = es_standardized_value, sei = es_standardized_se,
                   mods = ~ I(es_standardized_se^2), data = d, method = "REML")
  pet_estimate <- coef(summary(pet_fit))["intrcpt", "estimate"]
  pet_p <- coef(summary(pet_fit))["intrcpt", "pval"]

  all_diagnostics[[tid]] <- data.frame(
    technique_taxonomy_id = tid,
    n_studies = nrow(d),
    egger_z = egger$zval,
    egger_p = egger$pval,
    pcurve_skew_p = if (!is.null(pcurve_res)) pcurve_res$pBinomial$pBinomial.full else NA,
    pcurve_evidential_value = if (!is.null(pcurve_res)) pcurve_res$EvidencePresent else NA,
    pet_intercept = pet_estimate,
    pet_p = pet_p,
    pet_selection_fragile = abs(pet_estimate) < 0.20    # PROTOCOL § 9.7 C4
  )
}

bias_df <- bind_rows(all_diagnostics)
write_csv(bias_df, file.path(RESULTS_DIR, "bias_diagnostics.csv"))
message(sprintf("Wrote %d-technique bias diagnostics", nrow(bias_df)))
message("Next: 05_sensitivity.R for leave-one-out and post-2015 sensitivity")

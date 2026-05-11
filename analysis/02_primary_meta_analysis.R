# Closing Evidence Atlas — Phase 3 Primary Meta-Analysis
# Per-technique Bayesian random-effects model via brms + Stan.
#
# Implements PROTOCOL.md § 9.2 with weakly-informative priors:
#   y_i ~ Normal(theta_i, sigma_i)             # likelihood
#   theta_i ~ Normal(mu, tau)                  # study-level random effect
#   mu ~ Normal(0, 0.5)                        # weakly-informative on Hedges' g scale
#   tau ~ Half-Normal(0, 0.3)
#
# For binary-outcome techniques (log-OR scale):
#   mu ~ Normal(0, 0.7); tau ~ Half-Normal(0, 0.5)
#
# Convergence diagnostics: R-hat ≤ 1.01, ESS_bulk ≥ 1000, divergent transitions ≤ 1%.
#
# Run order (Phase 2 must be complete first):
#   1. Rscript analysis/01_load_and_validate.R
#   2. Rscript analysis/02_primary_meta_analysis.R
#   3. Rscript analysis/03_multiverse.R
#   4. Rscript analysis/04_bias_diagnostics.R
#   5. Rscript analysis/05_sensitivity.R
#
# Random seed: 20260510 (fixed and reported).
#
# Inputs:
#   data/standardized_effects.csv    — per-study standardized effect + SE
#   taxonomy/techniques.md           — survivor candidate list
#
# Outputs:
#   analysis/fits/<technique>.rds    — fitted brms model
#   results/posterior_summaries.csv  — posterior median + 95% CrI + P(mu>0) + tau
#   figures/forest_<technique>.pdf   — forest plot per technique
#   results/convergence_log.md       — R-hat, ESS, divergent counts
#
# Dependencies (install once):
#   install.packages(c("brms", "cmdstanr", "tidyverse", "bayesplot", "metafor"))
#   cmdstanr::install_cmdstan()
#
# Required versions:
#   R >= 4.4; brms >= 2.21; cmdstanr >= 0.8; Stan >= 2.34

suppressPackageStartupMessages({
  library(brms)
  library(cmdstanr)
  library(tidyverse)
  library(bayesplot)
})

set.seed(20260510)

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------
REPO <- here::here()
EFFECTS_PATH <- file.path(REPO, "data", "standardized_effects.csv")
FITS_DIR <- file.path(REPO, "analysis", "fits")
RESULTS_DIR <- file.path(REPO, "results")
FIGURES_DIR <- file.path(REPO, "figures")
TAXONOMY_PATH <- file.path(REPO, "taxonomy", "techniques.md")

dir.create(FITS_DIR, showWarnings = FALSE, recursive = TRUE)
dir.create(RESULTS_DIR, showWarnings = FALSE, recursive = TRUE)
dir.create(FIGURES_DIR, showWarnings = FALSE, recursive = TRUE)

# -----------------------------------------------------------------------------
# Pre-registered model specifications
# -----------------------------------------------------------------------------
# Per PROTOCOL § 9.2 — weakly-informative priors on Hedges' g and log-OR scales.

prior_g <- c(
  prior(normal(0, 0.5), class = "Intercept"),    # mu prior
  prior(normal(0, 0.3), class = "sd")            # tau prior (half-normal)
)

prior_logor <- c(
  prior(normal(0, 0.7), class = "Intercept"),
  prior(normal(0, 0.5), class = "sd")
)

# -----------------------------------------------------------------------------
# Survivor candidate techniques (from PROTOCOL § 9.7 C1: ≥ 5 included studies)
# -----------------------------------------------------------------------------
# Determined at Stage-1 + Stage-2 screening (see results/stage1_survivor_report.md).
# Updated as Stage-2 screening completes.

survivor_techniques <- c(
  "fitd", "ditf", "lowball", "gain-framing", "loss-framing",
  "regulatory-fit", "social-proof", "concrete-construal", "extreme-anchor",
  "commitment-consistency", "authority", "reciprocity", "scarcity",
  "disrupt-then-reframe"
)

# -----------------------------------------------------------------------------
# Helper: fit one technique
# -----------------------------------------------------------------------------
fit_one <- function(technique_id, effects_df, prior_set, outcome_scale = "g") {
  message(sprintf("[fit] %s (scale=%s)", technique_id, outcome_scale))
  technique_df <- effects_df %>% filter(technique_taxonomy_id == technique_id)
  n_studies <- nrow(technique_df)
  if (n_studies < 5) {
    warning(sprintf("Technique '%s' has only %d studies; below pre-registered threshold of 5. Skipping.", technique_id, n_studies))
    return(NULL)
  }

  fit <- brm(
    formula = es_standardized_value | se(es_standardized_se) ~ 1 + (1 | study_id),
    data = technique_df,
    prior = prior_set,
    family = gaussian(),
    chains = 4,
    iter = 4000,
    warmup = 2000,
    cores = 4,
    seed = 20260510,
    control = list(adapt_delta = 0.99, max_treedepth = 12),
    backend = "cmdstanr",
    refresh = 0
  )

  out_path <- file.path(FITS_DIR, sprintf("%s.rds", technique_id))
  saveRDS(fit, out_path)
  message(sprintf("  saved %s", out_path))
  fit
}

# -----------------------------------------------------------------------------
# Helper: extract posterior summary
# -----------------------------------------------------------------------------
summarize_fit <- function(fit, technique_id) {
  if (is.null(fit)) return(NULL)
  post <- posterior::as_draws_df(fit)
  mu_draws <- post$b_Intercept
  tau_draws <- post$sd_study_id__Intercept

  rhat_vals <- rhat(fit)
  ess_bulk <- posterior::ess_bulk(mu_draws)
  ess_tail <- posterior::ess_tail(mu_draws)
  ndiv <- sum(nuts_params(fit)$Value[nuts_params(fit)$Parameter == "divergent__"])

  # Posterior predictive interval per Higgins, Thompson, Spiegelhalter (2009)
  pred_low <- quantile(mu_draws + tau_draws * rnorm(length(mu_draws)), 0.025)
  pred_hi  <- quantile(mu_draws + tau_draws * rnorm(length(mu_draws)), 0.975)

  data.frame(
    technique_taxonomy_id = technique_id,
    n_studies              = nrow(fit$data),
    mu_median              = median(mu_draws),
    mu_ci_lower            = quantile(mu_draws, 0.025),
    mu_ci_upper            = quantile(mu_draws, 0.975),
    mu_ci90_lower          = quantile(mu_draws, 0.05),
    mu_ci90_upper          = quantile(mu_draws, 0.95),
    p_mu_gt_zero           = mean(mu_draws > 0),
    p_mu_gt_practical      = mean(mu_draws > 0.20),
    tau_median             = median(tau_draws),
    tau_ci_lower           = quantile(tau_draws, 0.025),
    tau_ci_upper           = quantile(tau_draws, 0.975),
    prediction_ci_lower    = pred_low,
    prediction_ci_upper    = pred_hi,
    rhat_max               = max(rhat_vals, na.rm = TRUE),
    ess_bulk               = ess_bulk,
    ess_tail               = ess_tail,
    n_divergent            = ndiv,
    converged              = (max(rhat_vals, na.rm = TRUE) <= 1.01) &&
                             (ess_bulk >= 1000) &&
                             (ndiv == 0)
  )
}

# -----------------------------------------------------------------------------
# Main loop
# -----------------------------------------------------------------------------
if (!file.exists(EFFECTS_PATH)) {
  stop(sprintf("Missing %s — run Phase 2 extraction first.", EFFECTS_PATH))
}

effects <- read_csv(EFFECTS_PATH, show_col_types = FALSE)
message(sprintf("Loaded %d standardized effects across %d techniques",
                nrow(effects), n_distinct(effects$technique_taxonomy_id)))

all_summaries <- list()
for (tid in survivor_techniques) {
  scale <- if (any(effects$es_standardized_metric == "log-odds-ratio" &
                  effects$technique_taxonomy_id == tid)) "logor" else "g"
  pr <- if (scale == "logor") prior_logor else prior_g
  fit <- tryCatch(fit_one(tid, effects, pr, scale),
                  error = function(e) { warning(e); NULL })
  s <- summarize_fit(fit, tid)
  if (!is.null(s)) all_summaries[[tid]] <- s
}

# -----------------------------------------------------------------------------
# Write posterior summaries
# -----------------------------------------------------------------------------
if (length(all_summaries) > 0) {
  summary_df <- bind_rows(all_summaries)
  summary_path <- file.path(RESULTS_DIR, "posterior_summaries.csv")
  write_csv(summary_df, summary_path)
  message(sprintf("Wrote %d-technique posterior summaries to %s", nrow(summary_df), summary_path))

  # Convergence log
  conv_log <- summary_df %>%
    select(technique_taxonomy_id, n_studies, rhat_max, ess_bulk, ess_tail,
           n_divergent, converged)
  conv_path <- file.path(RESULTS_DIR, "convergence_log.md")
  writeLines(
    c(
      "# Phase 3 Convergence Log",
      "",
      sprintf("Auto-generated %s by analysis/02_primary_meta_analysis.R", Sys.time()),
      "",
      "Acceptance criteria (per PROTOCOL § 9.2):",
      "- R-hat ≤ 1.01",
      "- ESS bulk and tail ≥ 1000",
      "- Divergent transitions = 0 (or ≤ 1% with adapt_delta increase)",
      "",
      "| Technique | k | R-hat | ESS bulk | ESS tail | Divergent | Converged |",
      "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
      apply(conv_log, 1, function(r) {
        sprintf("| `%s` | %s | %.3f | %s | %s | %s | %s |",
                r["technique_taxonomy_id"], r["n_studies"],
                as.numeric(r["rhat_max"]), r["ess_bulk"], r["ess_tail"],
                r["n_divergent"], r["converged"])
      })
    ),
    conv_path
  )
  message(sprintf("Wrote convergence log to %s", conv_path))
}

# -----------------------------------------------------------------------------
# Forest plots per technique
# -----------------------------------------------------------------------------
for (tid in names(all_summaries)) {
  fit <- readRDS(file.path(FITS_DIR, sprintf("%s.rds", tid)))
  pdf_path <- file.path(FIGURES_DIR, sprintf("forest_%s.pdf", tid))
  pdf(pdf_path, width = 7, height = max(5, nrow(fit$data) * 0.3))
  print(brms::pp_check(fit, type = "intervals", prob = 0.95) +
        ggplot2::ggtitle(sprintf("%s — observed vs posterior-predictive", tid)))
  dev.off()
  message(sprintf("Forest plot saved: %s", pdf_path))
}

message("Phase 3 primary meta-analysis complete.")
message("Next: 03_multiverse.R for specification-curve robustness.")

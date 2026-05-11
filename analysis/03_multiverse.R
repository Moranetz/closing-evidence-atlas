# Closing Evidence Atlas — Phase 4 Multiverse / Specification-Curve Analysis
# Implements PROTOCOL.md § 9.5: 486-specification cross-product per technique.
#
# Decisions varied:
#   1. Inclusion filter:    all-eligible / low-rob-only / pre-registered-only
#   2. Effect estimator:    hedges-g / log-or-where-convertible
#   3. Prior on mu:         Normal(0,0.5) / Normal(0,1) / Normal(0,0.1)
#   4. Outlier handling:    none / studentized-residual-2 / leave-one-out
#   5. Heterogeneity prior: Half-Normal(0,0.3) / Half-Cauchy(0,0.5) / Truncated-Normal(0,0.5)
#   6. Comparator restriction: any / inactive-only / active-only
#
# 3 × 2 × 3 × 3 × 3 × 3 = 486 specifications per technique.
#
# Survivor threshold: ≥ 80% of specifications produce 95% CrI excluding 0
# in the practitioner-claimed direction.
#
# Random seed: 20260510.

suppressPackageStartupMessages({
  library(brms)
  library(cmdstanr)
  library(tidyverse)
  library(furrr)         # parallel execution
})

set.seed(20260510)
plan(multisession, workers = parallel::detectCores() - 1)

REPO <- here::here()
EFFECTS_PATH <- file.path(REPO, "data", "standardized_effects.csv")
RESULTS_DIR <- file.path(REPO, "results")
FIGURES_DIR <- file.path(REPO, "figures")

source(file.path(REPO, "analysis", "_helpers.R"))  # shared fit helpers

# -----------------------------------------------------------------------------
# Define specification grid
# -----------------------------------------------------------------------------
inclusion_filters <- c("all-eligible", "low-rob-only", "pre-registered-only")
estimator_choices <- c("hedges-g", "log-or-where-convertible")
mu_priors <- list(
  weakly = c(0, 0.5),
  flat   = c(0, 1.0),
  skeptical = c(0, 0.1)
)
outlier_handling <- c("none", "studentized-residual-2", "leave-one-out")
tau_priors <- list(
  half_normal_03 = c("half-normal", 0.3),
  half_cauchy_05 = c("half-cauchy", 0.5),
  trunc_normal_05 = c("truncated-normal", 0.5)
)
comparator_restrictions <- c("any", "inactive-only", "active-only")

specs <- expand_grid(
  inclusion_filter = inclusion_filters,
  estimator = estimator_choices,
  mu_prior = names(mu_priors),
  outlier_handling = outlier_handling,
  tau_prior = names(tau_priors),
  comparator_restriction = comparator_restrictions
)
stopifnot(nrow(specs) == 3 * 2 * 3 * 3 * 3 * 3)
message(sprintf("Multiverse: %d specifications per technique", nrow(specs)))

# -----------------------------------------------------------------------------
# Run multiverse per technique
# -----------------------------------------------------------------------------
effects <- read_csv(EFFECTS_PATH, show_col_types = FALSE)
survivor_techniques <- intersect(
  read_csv(file.path(RESULTS_DIR, "posterior_summaries.csv"),
           show_col_types = FALSE)$technique_taxonomy_id,
  unique(effects$technique_taxonomy_id)
)

all_results <- list()
for (tid in survivor_techniques) {
  message(sprintf("[multiverse] %s — %d specs", tid, nrow(specs)))
  technique_data <- effects %>% filter(technique_taxonomy_id == tid)

  spec_results <- future_map_dfr(
    seq_len(nrow(specs)),
    function(i) {
      spec <- specs[i, ]
      d <- apply_spec_filters(technique_data, spec)
      if (nrow(d) < 5) return(NULL)
      fit <- tryCatch(
        fit_spec(d, spec, mu_priors, tau_priors),
        error = function(e) NULL
      )
      if (is.null(fit)) return(NULL)
      data.frame(
        spec_id = i,
        technique_taxonomy_id = tid,
        n_studies = nrow(d),
        inclusion_filter = spec$inclusion_filter,
        estimator = spec$estimator,
        mu_prior = spec$mu_prior,
        outlier_handling = spec$outlier_handling,
        tau_prior = spec$tau_prior,
        comparator_restriction = spec$comparator_restriction,
        mu_median = median(posterior::as_draws_df(fit)$b_Intercept),
        mu_ci_lower = quantile(posterior::as_draws_df(fit)$b_Intercept, 0.025),
        mu_ci_upper = quantile(posterior::as_draws_df(fit)$b_Intercept, 0.975)
      )
    },
    .options = furrr_options(seed = TRUE)
  )

  all_results[[tid]] <- spec_results
}

# -----------------------------------------------------------------------------
# Compute survivor threshold per technique
# -----------------------------------------------------------------------------
multiverse_summary <- map_dfr(all_results, function(df) {
  if (nrow(df) == 0) return(NULL)
  excludes_zero <- df$mu_ci_lower > 0 | df$mu_ci_upper < 0
  data.frame(
    technique_taxonomy_id = df$technique_taxonomy_id[1],
    n_specifications = nrow(df),
    pct_excluding_zero = 100 * mean(excludes_zero),
    median_of_medians = median(df$mu_median),
    spec_curve_lower = quantile(df$mu_median, 0.05),
    spec_curve_upper = quantile(df$mu_median, 0.95),
    multiverse_survivor = mean(excludes_zero) >= 0.80   # PROTOCOL § 9.5 threshold
  )
})

write_csv(multiverse_summary, file.path(RESULTS_DIR, "multiverse_summaries.csv"))
walk(names(all_results), function(tid) {
  write_csv(all_results[[tid]], file.path(RESULTS_DIR, sprintf("multiverse_spec_%s.csv", tid)))
})
message("Multiverse complete.")
message("Next: 04_bias_diagnostics.R for funnel plots, Egger, p-curve, three-parameter selection.")

# Closing Evidence Atlas — Phase 4 Sensitivity Analyses
# Implements PROTOCOL.md § 9.6:
#   1. Excluding high-RoB studies
#   2. Leave-one-out per technique
#   3. Post-2015 only (post replication-crisis era)
#   4. Pre-registered only
#   5. Direct conceptual replications
#   6. Industry-funded vs independent split
#
# Each sensitivity is reported alongside primary estimate.
# Substantive divergence (> 50% shrinkage in posterior median) is flagged.
#
# Random seed: 20260510.

suppressPackageStartupMessages({
  library(brms)
  library(cmdstanr)
  library(tidyverse)
})

set.seed(20260510)
REPO <- here::here()
EFFECTS_PATH <- file.path(REPO, "data", "standardized_effects.csv")
RESULTS_DIR <- file.path(REPO, "results")

source(file.path(REPO, "analysis", "_helpers.R"))

prior_g <- c(
  prior(normal(0, 0.5), class = "Intercept"),
  prior(normal(0, 0.3), class = "sd")
)

effects <- read_csv(EFFECTS_PATH, show_col_types = FALSE)
posterior_summary <- read_csv(file.path(RESULTS_DIR, "posterior_summaries.csv"),
                              show_col_types = FALSE)

primary_medians <- setNames(posterior_summary$mu_median,
                            posterior_summary$technique_taxonomy_id)

# -----------------------------------------------------------------------------
# Sensitivity helpers
# -----------------------------------------------------------------------------
refit_subset <- function(df, label) {
  if (nrow(df) < 5) return(data.frame(label = label, mu_median = NA,
                                       mu_ci_lower = NA, mu_ci_upper = NA,
                                       n_studies = nrow(df)))
  fit <- brm(
    formula = es_standardized_value | se(es_standardized_se) ~ 1 + (1 | study_id),
    data = df, prior = prior_g, family = gaussian(),
    chains = 4, iter = 4000, warmup = 2000, cores = 4,
    seed = 20260510, refresh = 0,
    backend = "cmdstanr",
    control = list(adapt_delta = 0.99)
  )
  mu <- posterior::as_draws_df(fit)$b_Intercept
  data.frame(
    label = label,
    mu_median = median(mu),
    mu_ci_lower = quantile(mu, 0.025),
    mu_ci_upper = quantile(mu, 0.975),
    n_studies = nrow(df)
  )
}

# -----------------------------------------------------------------------------
# Per-technique sensitivity
# -----------------------------------------------------------------------------
all_sens <- list()
for (tid in posterior_summary$technique_taxonomy_id) {
  message(sprintf("[sensitivity] %s", tid))
  d <- effects %>% filter(technique_taxonomy_id == tid)
  if (nrow(d) < 5) next

  # 1. Low-RoB only
  low_rob <- d %>% filter(rob_overall %in% c("low", "some-concerns"))
  s1 <- refit_subset(low_rob, "low-rob-only")

  # 2. Leave-one-out — report range of medians
  loo_medians <- sapply(seq_len(nrow(d)), function(i) {
    out <- refit_subset(d[-i, ], sprintf("loo-%d", i))
    out$mu_median
  })
  s2 <- data.frame(
    label = "loo-range",
    mu_median = NA,
    mu_ci_lower = min(loo_medians, na.rm = TRUE),
    mu_ci_upper = max(loo_medians, na.rm = TRUE),
    n_studies = nrow(d)
  )

  # 3. Post-2015 only
  post2015 <- d %>% filter(as.integer(year) >= 2015)
  s3 <- refit_subset(post2015, "post-2015-only")

  # 4. Pre-registered only
  preregistered <- d %>% filter(pre_registered %in% c("yes-osf", "yes-aea", "yes-other"))
  s4 <- refit_subset(preregistered, "pre-registered-only")

  # 5. Direct conceptual replications
  replications <- d %>% filter(is_replication == TRUE)
  s5 <- refit_subset(replications, "direct-replication-only")

  # 6. Industry-funded split
  industry <- d %>% filter(funding_source_type == "industry")
  s6_industry <- refit_subset(industry, "industry-funded-only")
  independent <- d %>% filter(funding_source_type != "industry")
  s6_indep <- refit_subset(independent, "independent-funded-only")

  all_sens[[tid]] <- bind_rows(s1, s2, s3, s4, s5, s6_industry, s6_indep) %>%
    mutate(technique_taxonomy_id = tid,
           primary_median = primary_medians[tid],
           shrinkage_pct = 100 * (1 - mu_median / primary_median))
}

sens_df <- bind_rows(all_sens)
write_csv(sens_df, file.path(RESULTS_DIR, "sensitivity_analyses.csv"))
message("Sensitivity analyses complete.")

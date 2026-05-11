# Closing Evidence Atlas — Phase 2 Data Loading + Validation
# Loads data/extracted_studies.csv, standardizes effect sizes to Hedges' g
# (continuous) or log-OR (binary) per PROTOCOL § 7.3, and produces
# data/standardized_effects.csv used by all Phase 3 + Phase 4 scripts.

suppressPackageStartupMessages({
  library(tidyverse)
  library(metafor)
})

REPO <- here::here()
EXTRACTED_PATH <- file.path(REPO, "data", "extracted_studies.csv")
PILOT_PATH <- file.path(REPO, "data", "extracted_studies_pilot.csv")
OUT_PATH <- file.path(REPO, "data", "standardized_effects.csv")

# Use full extracted set if present; else fall back to pilot
input_path <- if (file.exists(EXTRACTED_PATH)) EXTRACTED_PATH else PILOT_PATH
if (!file.exists(input_path)) {
  stop(sprintf("Neither %s nor %s exists — run Phase 2 extraction first.",
               EXTRACTED_PATH, PILOT_PATH))
}
message(sprintf("Loading from %s", input_path))

raw <- read_csv(input_path, show_col_types = FALSE)

# -----------------------------------------------------------------------------
# Effect-size standardization per PROTOCOL § 7.3
# -----------------------------------------------------------------------------
# Where a study reports raw means + SDs, convert via metafor::escalc(measure="SMD")
# Where binary outcomes are reported, convert via measure="OR"
# Where Pearson r is reported, convert via Fisher's z then SMD
# Where F or t reported, reconstruct via Borenstein et al. 2009 Ch. 7

# This pilot uses effect sizes already standardized in the extraction step;
# real Phase 2 will need per-row conversion logic. The skeleton:

raw_std <- raw %>%
  filter(!str_detect(rob_notes, "STAGE-2 EXCLUDE")) %>%
  rowwise() %>%
  mutate(
    es_metric_class = case_when(
      str_detect(effect_size_metric, "cohen-d|hedges-g|standardized") ~ "smd",
      str_detect(effect_size_metric, "log-odds-ratio|odds-ratio") ~ "logor",
      str_detect(effect_size_metric, "eta-squared|eta-partial-squared") ~ "eta-squared",
      str_detect(effect_size_metric, "F-statistic|F-statistics") ~ "F-statistic",
      str_detect(effect_size_metric, "beta|unstandardized") ~ "beta-unstandardized",
      TRUE ~ "other-needs-conversion"
    ),
    es_standardized_value = case_when(
      es_metric_class == "smd" ~ as.numeric(effect_size_value),
      # eta-squared → Cohen's d conversion: d = 2*sqrt(eta²/(1-eta²))
      es_metric_class == "eta-squared" ~ 2 * sqrt(as.numeric(effect_size_value) /
                                                   (1 - as.numeric(effect_size_value))),
      TRUE ~ NA_real_
    ),
    es_standardized_se = case_when(
      es_metric_class == "smd" & !is.na(effect_size_ci_upper) & !is.na(effect_size_ci_lower) ~
        (as.numeric(effect_size_ci_upper) - as.numeric(effect_size_ci_lower)) / (2 * 1.96),
      TRUE ~ NA_real_
    )
  ) %>%
  ungroup()

# For pilot demonstration, flag rows that need full conversion logic
incomplete <- raw_std %>% filter(is.na(es_standardized_value) | is.na(es_standardized_se))
message(sprintf("Records needing additional conversion logic: %d / %d",
                nrow(incomplete), nrow(raw_std)))

write_csv(raw_std %>% select(study_id, technique_taxonomy_id, year, n_total,
                              es_standardized_value, es_standardized_se,
                              rob_overall, pre_registered, funding,
                              everything()), OUT_PATH)
message(sprintf("Wrote %d standardized effects to %s", nrow(raw_std), OUT_PATH))

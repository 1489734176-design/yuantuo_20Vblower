# Progress

- 2026-11-05: Inspected current acquisition, calibrated conversion, regulator and duty bounds. User authorized continuing.
- Identified installed Keil UV4 plus AC5 and AC6. Plan isolated builds to preserve existing output files.
- Enabled LIMIT_AVG_CURRENT_EN and aliased every average-current limit to CONSTANT_BUS_CURRENT=28.0f. Only production diff: USER/inc/parameter.h, 8 additions / 6 deletions.
- UV4 project-copy invocation failed before compilation (exit 15); direct installed compiler builds succeeded for both versions. Logs and outputs are in ac5-direct and ac6-direct.
- AC5 clean rebuild: 35 sources, 1 core library, 0 warnings / 0 errors; code 16688, RO-data 224, RW-data 152, ZI-data 1528 bytes.
- AC6 clean rebuild: 35 sources, 1 core library, 32 reviewed pre-existing warnings / 0 errors; code 16576, RO-data 224, RW-data 68, ZI-data 1556 bytes.
- Examined compiled pwm_set offset/gain/current comparison, recovery and decreasing branches. Independent reviewer found no blocker and identified expected duty-limit/calibration/transient limitations.
- Original KEIL_PRJ generated and IDE files were not changed by these builds. git diff --check passed for the production header. No bench test or flashing performed.

# 28A current regulation

User requirement: add 28A constant-current behavior. The implementation uses the existing average bus current PWM feedback, in the active USER/inc/parameter.h configuration. All direction/gear thresholds share one 28.0A macro.

## Approaches
Reuse the existing sampled-current regulator: smallest change, retains calibrated sampling and the tested ramp/duty bounds. A new PI regulator would require gain tuning and board transient measurements not supplied in this task. Selected implementation: reuse the existing regulator, as stated to the user before implementation; user requested continuing.

## Behavior and constraints
Above 28A the regulator decreases duty; below 28A it recovers toward the trigger/gear command. Minimum/maximum duty, startup, overcurrent, temperature, undervoltage, watchdog and stall protections retain their existing behavior. Light loads and low trigger commands may consume less than 28A; regulation accuracy and transient overshoot require bench measurements. The active header is changed; parameter-300N.h is a separate product reference.

Verification: clean AC6 rebuild and review the compiled pwm_set current comparison. Preserve existing generated and IDE modifications by building in the task directory. Hardware revision, supply, load, current calibration and measured safety behavior must be recorded during board validation.

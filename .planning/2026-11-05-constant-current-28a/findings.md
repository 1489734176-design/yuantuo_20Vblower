# Findings

- Active compiled header: USER/inc/parameter.h. Root parameter-300N.h is a separate reference set.
- pwm_set() already compares calibrated ADC4 average current against a direction/gear threshold, reducing PWM above it and recovering below it at 16kHz with the existing six-tick, one-count slope.
- LIMIT_AVG_CURRENT_EN is currently 0; thresholds are 15A/25A/35A/35A CW and 36A CCW.
- RSHUNT=1mOhm, AMPLIFICATION_GAIN=10.89, ADC_REFV=5V, ADC_REF_VALUE=4095: 28A threshold truncates to 249 ADC counts. Offset subtraction and Q15 Vcc_cal_gain already occur before comparison.
- Minimum PWM remains 15%; regulation can saturate at the permitted duty bounds. Light-load or reduced-trigger operation does not force current to 28A. Transient peaks are handled by existing protections.
- uvprojx actually selects AC5.06, while AGENTS.md requires AC6. Both toolchains exist under D:/Users/mym02/AppData/Local/Keil_v5/ARM.
- Git main contains existing generated/IDE changes only. No source baseline modifications found.
- Clean direct builds compile 35 project C/assembly units and link the existing HS core library in the configured 32KB flash / 4KB RAM layout. AC5: 0 errors, 0 warnings, code 16688 bytes. AC6: 0 errors, 32 warnings (31 original header filename case warnings plus deprecated legacy armasm), code 16576 bytes. No warnings concern the new target or enabled current comparison.
- AC6 pwm_set machine code at 0x08003ad4 retains offset subtraction and VCC multiplication. Optimizer checks the high product bits against 125 (half-scaled), equivalent to calibrated current >=250 counts, i.e. >249-count configured target. The six-tick PWM decrease, command-bounded recovery and duty floor/ceiling remain present.
- Narrow independent review found no implementation blocker, and confirmed practical limits: light load / reduced trigger demand, minimum PWM saturation, calibration accuracy, current ripple and transient delay. Protections and thresholds are unchanged.

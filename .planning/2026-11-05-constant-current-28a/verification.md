# 28A current regulation verification

Production change: USER/inc/parameter.h enables calibrated average bus-current PWM feedback and assigns all five threshold selections to CONSTANT_BUS_CURRENT=28.0f. Existing protection logic/thresholds and minimum/maximum PWM are unchanged.

## Builds
Run `python -I .planning/2026-11-05-constant-current-28a/build_direct.py --variant ac6` (or ac5). The script compiles all 35 sources from the Keil source list using installed Keil tools and links the existing library with the project's flash/RAM layout and microlib ABI. Logs record exact commands. UV4 project copies could not launch their build (exit 15), so the IDE wrapper itself was not validated.

| Compiler | Errors | Reviewed warnings | Code bytes | RW + ZI bytes |
|---|---:|---:|---:|---:|
| AC5 5.06 update 7 | 0 | 0 | 16688 | 1680 |
| AC6 6.22 | 0 | 32: existing header filename casing + deprecated legacy assembler | 16576 | 1624 |

Both builds fit the 32KB flash / 4KB RAM device limits. The compiled PWM routine contains the calibrated >249 ADC count comparison, downward PWM step and command-bounded upward recovery. Independent source review found no blocker.

## Required board measurements (not performed)
Record board/hardware revision, shunt value and amplifier gain, supply voltage, motor/load and active parameters. Check actual input current against calibrated ADC readings. Increase load gradually to observe steady regulation near 28A, then measure ripple, overshoot and settling under load steps. Check low trigger settings, maximum duty and minimum-duty saturation. Verify trigger release/restart and the existing current, undervoltage, thermal, watchdog and stall protections. Record current/PWM waveforms and faults.

The 28A value is a target for the existing regulator, not measured precision or an instantaneous hard ceiling. Light load / reduced trigger demand may remain below it; minimum PWM may prevent reducing heavy-load current to it. Original protections remain the final fault handling path.

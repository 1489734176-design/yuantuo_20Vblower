# 28A constant-current task

## Goal
Enable the existing calibrated average-bus-current PWM regulation at 28A in the active product parameter header.

## Phases
- [x] Inspect current acquisition, PWM regulator, safety gates and build configuration.
- [x] Set one shared 28A target and enable all existing average-current limit selections.
- [x] Clean rebuild with Arm Compiler 6; inspect warnings and regulator machine code.
- [x] Review source-only diff and provide firmware plus bench verification requirements.

## Decisions
- User requested the feature and then said “继续”; proceed in the requested workspace.
- Reuse the existing PWM regulator rather than add an uncalibrated PI loop.
- Preserve trigger/gear duty bounds, startup, protections and reference parameter-300N.h.
- Keep existing generated and IDE modifications intact; build into this task's directory.
- Configuration-only change: validate compiled regulator and build instead of introducing a host test framework.

## Errors Encountered
- Two read-only subagents were stopped by a service rate limit; root completed the inspection.
- UV4 rejected both isolated project copies with exit code 15 before producing a log. Removing -j0 did not resolve it. Bypassed the IDE launcher by clean-building all project sources with the installed Keil compiler/assembler/linker tools. No source workaround was needed.
- Direct compiler preflight first missed the CMSIS include directory; corrected to the repository's CMSIS/Core/Include.

## Next Step
Software changes and build verification complete. Bench measurements remain required on the intended board; no flashing or hardware test was performed in this task.

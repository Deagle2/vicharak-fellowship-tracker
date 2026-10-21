# Projects index — check before you submit

*Maintained by the admin. Last updated 2026-10-20.*

Before you submit a **Project**, check both lists below. If your idea is already
here or in the upstream examples, pick something different — otherwise the PR
gets closed and you score 0 for it.

> **Rule:** your project must be your own work on top of the board, not a copy of
> an upstream example. If you build on an example, extend it meaningfully
> (new peripherals, real-world use, custom toolchain, your own docs) and say so
> in the PR description.

## 1. Projects already accepted in this program (7)

| Fellow | Project | Link |
|---|---|---|
| Adeep AG | Geto Web IDE : For Shrike Series board(RP2040 & RP2350) | https://github.com/ADEEP13/IDE |
| ANNESTIO PIETY CASTANHA | ShrikeFi 16-bit Multicycle CPU | https://github.com/apcetc/Vicharak_Campus_Fellowship_APC-/tree/main/PROJECT_1 |
| Nathan Mathews | Tiny ILA for Shrike | https://github.com/Deagle2/shrike-traces |
| Revand Pradeep | Shrike-Sentinel | https://docs.google.com/document/d/1DzsEX9RhsuA5Obxm0qkuIky-P2YCXNoWIiYl_c4sDtA/edit?usp=sharing |
| Saksham Sud | Perch — Passive Environmental Radio Census for ShrikeFi (receive-only 802.11 management-frame auditor) | https://github.com/Geneticscrol/perch |
| Saksham Sud | ShrikeFi BLE find-my-board tag (iBeacon + Find Me + last-seen map) | https://github.com/Geneticscrol/shrikefi-ble-tag |
| yatharth vishwa | OTA support for ShrikeFi's FPGA | https://github.com/yatharthvishwa/ShrikeFi_FPGAOTA |

*(This list is also visible in [`submissions/INDEX.md`](../submissions/INDEX.md), which regenerates on every merge.)*

## 2. Upstream example projects in `vicharak-in/shrike` (32)

These are the official examples. **Do not submit these as your own project** —
build your own version instead.

`breathing_led` · `button_debouncer` · `cordic` · `counter_4bit` · `dspi_pio_echo` ·
`gpio_extender_14pin` · `gpio_extender_8pin` · `i2c_led` · `led_blink` ·
`led_reaction_timer` · `logic_gates` · `morse_blink` · `pll_oscillator` ·
`pmod_dual_7seg` · `pmod_led_blink` · `pmod_led_patterns` · `protocol_translator` ·
`pwm_4ch` · `quadrature_decoder` · `shrike_picorv32` · `shrike_picorv32_xip` ·
`shrike_serv` · `spi_loopback_led` · `spi_to_usb` · `stack_processor` · `uart_led` ·
`uart_sum` · `ultrasonic_sensor` · `usb_to_spi` · `vector4_cpu` · `vector8_cpu` ·
`ws2812_led`

Browse them: https://github.com/vicharak-in/shrike/tree/main/examples

## 3. Ideas that are still open

- ShrikeFi **ESP32-S3** projects: WiFi/BLE bring-up, sensor dashboards, OTA on ESP32 side
- **Vaaman / Axon** boards (not yet used by anyone)
- Shrike Lite **battery / power profiling**, USB-C PD bring-up
- **OpenFPGA / soft-core** builds beyond the upstream `shrike_picorv32`
- **ShrikeFi OTA** (upstream board support exists — build an app/firmware on top)
- Anything with **Pmod** peripherals, cameras, SDR, audio
- A **Shrike-FI cluster** or multi-board project

## 4. If your PR gets closed

The admin closes a Project PR when:

1. It duplicates an upstream example or a project in section 1 — **fix and resubmit** (see below).
2. The JSON is invalid (wrong `fellow`, bad `link`, missing `.json` extension) — **fix and resubmit**.
3. The PR carries bot-generated files (you ran the scorer locally) — **clean your branch and resubmit**.

Full resubmission guide: [`docs/FORKS.md`](FORKS.md)

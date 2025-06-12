
## Default Parameters
Output and measurement configuration details:
| DB0 (n) | Signals    | Default MODE | Default TIME [ms] | Min TIME [ms] | Description                                                                       |
| ------- | ---------- | ------------ | ----------------- | ------------- | --------------------------------------------------------------------------------- |
| 0       | Current    | Cyclic       | 20                | 1             | output-cycle-time = Measurement-interval                                          |
| 1       | U1         | Cyclic       | 60                | 3             | output-cycle-time = Measurement-interval (depending on configuration of U1 .. U3) |
| 2       | U2         | Cyclic       | 60                | 3             | output-cycle-time = Measurement-interval (depending on configuration of U1 .. U3) |
| 3       | U3         | Cyclic       | 60                | 3             | output-cycle-time = Measurement-interval (depending on configuration of U1 .. U3) |
| 4       | T          | Disable      | 100               | 1             | Output-cycle-time, Measurement-interval = 100 ms                                  |
| 5       | P in WU1   | Disable      | 30                | 6             | Output-cycle-time, Measurement-interval = 30 ms                                   |
| 6       | Q in As    | Disable      | 30                | 1             | Output-cycle-time, Measurement-interval = 30 ms                                   |
| 7       | ΔE in WhU1 | Disable      | 30                | 1             | Output-cycle-time, Measurement-interval = 30 ms                                   |

## Messages Overview
| Description       | Default CAN-ID | Default Endian | Length DLC | Remark                                                                                      |
| ----------------- | -------------- | -------------- | ---------- | ------------------------------------------------------------------------------------------- |
| IVT_Msg_Command   | 0x411          | Big Endian     | 8          | Function commands, SET and GET commands. A command-ID-byte is included for identification   |
| IVT_Msg_Debug     | 0x510          | -              | 8          | Message only for internal use                                                               |
| IVT_Msg_Response  | 0x511          | Big Endian     | 8          | Response to SET and GET command messages. A response-ID-byte is included for identification |
| IVT_Msg_Result_I  | 0x521          | Big Endian     | 6          | Current                                                                                     |
| IVT_Msg_Result_U1 | 0x522          | Big Endian     | 6          | Voltage 1                                                                                   |
| IVT_Msg_Result_U2 | 0x523          | Big Endian     | 6          | Voltage 2                                                                                   |
| IVT_Msg_Result_U3 | 0x524          | Big Endian     | 6          | Voltage 3                                                                                   |
| IVT_Msg_Result_T  | 0x525          | Big Endian     | 6          | Temperature                                                                                 |
| IVT_Msg_Result_W  | 0x526          | Big Endian     | 6          | Power (referring to current and voltage U1)                                                 |
| IVT_Msg_Result_As | 0x527          | Big Endian     | 6          | Current counter                                                                             |
| IVT_Msg_Result_Wh | 0x528          | Big Endian     | 6          | Energy counter (referring to current and  voltage U1)                                       |

- Not used bytes in response messages are undefined and reported as 0x00.
- Not used / undefined bytes in command messages must be set to 0x00.
- Each defined command will report its response message even if there was no change done or is currently
not allowed (e.g. set configuration during run mode). This is done to give acknowledge to the sender.
- Consecutive commands must be sent not faster than 2 ms, or you can wait until the related response is
sent.
- Response messages must be available on the bus (free bus) at least +500 ms after the related command,
if not otherwise specified.

## Result Messages
| DB | Signal | Value | Description |
|----|--------|-------|-------------|
| 0 | MuxID | 0x00 .. 0x07 | multiplexer, n = channel number |
| 1 (Low nibble) | IVT_MsgCount | 0x0 .. 0xF | Cyclic counter individually for each channel |
| 1 (High nibble) | IVT_Result_state | 0b0000 .. 0b1111 | bit 0: set if OCS is true<br>bit 1: set if<br>- this result is out of (spec-) range,<br>- this result has reduced precision<br>- this result has a measurement-error<br>bit 2: set if<br>- any result has a measurement-error<br>bit 3: set if<br>- any result has a system-error<br>→ sensor functionality is not ensured! |
| 2 .. 5 | IVT_<Resultname> | - | All Results as signed long, see configuration |




- Independent of the measurement and system error bit masks (s. chapter 8.4. and 8.6.), bit 2 and 3
can always occur due to CRC errors. Bit 2 also in case of Vref errors.
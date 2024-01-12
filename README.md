# ele

> `pip install -e .` # install as module using pip

> python setup.py develop (adds 'ele', 'ele_source', and 'ele_main' to $PATH)

### ipc protocol
> Single bytes are small but can represent different things depending on how we interpret them.

> An ASCII character like 'a' would be 97.

> A header field like protocol version might be 2 bytes 0x01 0x00.

> Raw payload data could be any sequence of bytes.

> Protocols define how to interpret byte sequences - this lets many different types of data be transmitted unified as bytes.

> Network protocols organize data into discrete packages called packets for transmission.

> A packet contains header fields like source/destination followed by payload data.

> In Python, we can represent this packet as a bytes object - the header as initial bytes and payload at the end.

> Sending/receiving sockets deal with bytes, matching how packets are transmitted on networks.

So in summary, bytes objects let us work with network data exactly as it is transmitted - as raw individual bytes that higher level protocols and code can interpret meaningfully. 

#### tinyframe schema

```
Header (1 byte):

Only 2 possible values:
0x01 = Request frame
0x02 = Response frame
This byte identifies the frame type at the beginning
Requests use 0x01, Responses use 0x02
Only these 2 values are allowed to clearly delimit the frame type
Length (1 byte):

Stores the number of bytes in the Payload field as a single byte (range 0-255)
Length can vary between frames but is limited to 255 bytes max
Reader knows how many Payload bytes to expect based on this field
Payload:

Format varies based on frame Header type (Request vs Response)
Request Payload:

Command (1 byte):
Possible commands 0x01, 0x02, etc (values TBD)
Identifies the action/operation the Request represents
Args (optional bytes):
Additional data for the specific Command
Only included if relevant to that Command
Response Payload:

Status (1 byte):
Success/Error codes 0x00, 0x01, 0x02 (custom values can be set)
Indicates result of processing the corresponding Request
Data (optional bytes):
Only included for successful Responses
Contains any data returned for the Request
Footer (1 byte):

Matches Header byte to clearly mark frame boundary
0x01 for Request, 0x02 for Response
```


### broker subarchitecture
A data broker typically uses a publish-subscribe model to facilitate one-to-many asynchronous data where:

> Producers "publish" data to topics

> Consumers "subscribe" to topics to receive relevant data

> Brokers handle persistence/distribution, protocols just transit data between endpoints

> Brokers define topic-based filters, protocols define format/semantics of messages

> Subscriptions in brokers, addresses/ports in protocols to identify communication peers

> Data brokers enable pub-sub distribution via topics

Protocols differ because they enable direct two-way data exchange between known endpoints. The kernel and Python runtime would use a protocol for synchronous request-response style IPC. A broker could later subscribe to their requests/responses for additional distribution/persistence.

### monitoring, error-checking
> Define a protocol specifying the byte-level serialization format
> Broker function on Python side packs data into bytes per protocol
> Kernel function unpacks bytes back into native data types
> Async I/O via select()/pipe for non-blocking transfer
> Logging utils see raw bytes for protocol verification


### ele-sql

The binary encoding standard such that bytes can be cat together chronologically (either real time, or 'fake' t=time) to form a single BLOB.

> Individual cells are BLOBs which are cat together chronologically to form a single UFX object which is like a superposition of UFS objects, BYTES, states, and NLP vector embeddings

> CELLs automatically (tick-based chrono-queue which ensures chrono-ordering) write to the sql db, until the end of the db is reached at which point the next CELL overwrites the zeroth and continues rewriting from there.

``` # 't' is a timestamp-type of .ufs object which is a 32-bit integer cat onto the frame of the BLOB
<runtime operations>
        |10|
        |11|
        |01|    # state is a complimentary binary filetype (.ele)
        |11|
        |01|
<monolithic messaging broker>  # reads from state, runtime, .ele, BLOBs, and .ufs objects
<python runtime> ========> <state> <============= <ele> # continuously re-written BLOBs written into elesql db restarting and rewriting each-time the end is reached
<monolithic messaging broker>  # writes to .ele, BLOBs, and .ufs objects
        |10|
        |11|
        |01|    # state can be rewritten in the middle of a BLOB
        |11|
        |01|
<underlying ufs objects>
<elesql db (no state and no 't'=time to fascilitate continous re-write of BLOBs and 'Halting Problem' kernel panicing)>
```

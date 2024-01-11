# ele
`pip install -e .` # install as module using pip



> Single bytes are small but can represent different things depending on how we interpret them:
> An ASCII character like 'a' would be 97.
> A header field like protocol version might be 2 bytes 0x01 0x00.
> Raw payload data could be any sequence of bytes.
> Protocols define how to interpret byte sequences - this lets many different types of data be transmitted unified as bytes.
> Bytes used for network packets:

> Network protocols organize data into discrete packages called packets for transmission.
> A packet contains header fields like source/destination followed by payload data.
> In Python, we can represent this packet as a bytes object - the header as initial bytes and payload at the end.
> Sending/receiving sockets deal with bytes, matching how packets are transmitted on networks.
> So in summary, bytes objects let us work with network data exactly as it is transmitted - as raw individual bytes that higher level protocols and code can interpret meaningfully. 




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

### broker subarchitecture
A data broker typically uses a publish-subscribe model to facilitate one-to-many asynchronous data where:
        Producers "publish" data to topics
        Consumers "subscribe" to topics to receive relevant data
        Brokers handle persistence/distribution, protocols just transit data between endpoints
        Brokers define topic-based filters, protocols define format/semantics of messages
        Subscriptions in brokers, addresses/ports in protocols to identify communication peers
        Data brokers enable pub-sub distribution via topics
Protocols differ because they enable direct two-way data exchange between known endpoints. The kernel and Python runtime would use a protocol for synchronous request-response style IPC. A broker could later subscribe to their requests/responses for additional distribution/persistence.
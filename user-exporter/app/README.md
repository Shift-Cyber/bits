# Bits User Connector
The intent of this worker is to tunnel the Arcustech Craft userbase to a local mysql repositry accessible by the bits Discord bot. The allows the bot to process registration requests by users in realtime. Eventually the database is going to be migrated to GCP but until that time this worker is necessary. This code is a bit hacky (specifically the threading is kinda jank) but it does what it needs to.

## Environment Variables
| Environment Variable | Description                        | Required | Default    |
| -------------------- | ---------------------------------- | -------- | ---------- |
| WORKER_INTERVAL_SEC  | Seconds to wait before re-running  | Yes      |            |
| SSH_PASSWD           | SSH cred for the arcustech server  | Yes      |            |
| SSH_USER             | SSH user for the arcustech server  | Yes      |            |
| SSH_HOST             | Arcustech public interface         | Yes      |            |
| ARC_DB_USER          | Arcustec mysql database user       | Yes      |            |
| ARC_DB_PASS          | Arcustec mysql database password   | Yes      |            |
| BITS_DB_HOST         | The bits database public interface | Yes      |            |
| BITS_DB_USER         | The bits database username         | Yes      |            |
| BITS_DB_PASS         | The bits database password         | Yes      |            |
| BITS_DB              | The bits database                  | No       | hack_a_bit |
| BITS_DB_PORT         | The bits database port             | No       | 3306       |
| CONNECTOR_HOST       | Local MYSQL connector host         | No       | 127.0.0.1  |
| CONNECTOR_PORT       | Local MYSQL connector port         | No       | 3336       |
| ARC_HOST             | Arcustec mysql host via forward    | No       | 127.0.0.1  |
| ARC_PORT             | Arcustec db port                   | No       | 3336       |
| THREAD_COUNT         | Number of parallel threads to run  | No       | 25         |

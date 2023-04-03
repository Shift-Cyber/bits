![SCYCA Logo](.rsrc/git-banner.png)
# Bits
Humanoid Discord bot with too much power and a bit of an attitude...

## Overview
This is the main development repository for the Bits discord bot. Bits is the Discord bot for Shift Cyber's Hack-a-Bit Capture the Flag (CTF) competition. Please submit pulls to add additional features if you have cool ideas. We are always accepting new volunteers to help with open-source maintenance. If you have found a vulnerability, please consider responsible disclosure via our main contact contact@shiftcyber.com. **Do not submit pull requests related to vulnerabilities.** We will credit you on the repository if you have a hand in development or security. Thanks for checking out the Bot, hope to see you participating in a competition in the future and/or volunteering to help us inspire the next generation of security experts.


## Development
### Branch Protection
By default, the production branch of bits is protected and only allows administrators to pull down. Release branches are also protected but anyone may submit a pull request to be reviewed by administrators. Administrators must approve a pull before it can be merged into a feature branch. Once requirements for a production release of bit are met, the branch is merged down to production and the old feature branches should be purged. Release branches are named release/\* and development branches should be named \<name\>/\<brief-feature-description\>. If they are not, an administrator may ask you to rename your feature branch for CI/CD clarity.

### Core Contributors
#### [Darian Arnold](discord://discordapp.com/users/277500700496363521)
Darian Arnold is a lead developer and the infrastructure management supervisor during Hack a Bit Competition. He has had a major hand in development of the bot and can take any questions related to bot setup, execution and development. Specifically he has done substnatial work on bot commands and therefor is the primary contact for that aspect of the bot.

#### [Nate Singer](discord://discordapp.com/users/523958300396748810)
Nate Singer is the founder of Shift Cyber and is the primary point of contact for this bot. He is resposible for most of the staging code and the framework for the bot. Therefor if there are questions related to environment or complxities in that arean, he should be the primary point of contact.


## Requirements
Bits is implemented via Discord's developer API which you can find at the following URL: https://discord.com/developers/docs/intro. The interface is written using the Discord.py libraries and a Cog system. The current Bits deployment was tested and deployed with Python 3.10. You can see more detail about the requirements in the Docker build scripts.


## Repository Breakdown
```
├── app                 <-- All bot-related source and depends
│   ├── cogs            <-- Cogs to handle all commands
│   ├── connectors      <-- Database and email connectors
│   ├── sql-scripts     <-- Various sql scripts for database testing
│   └── structures      <-- Structs in use across the application
├── user-exporter       <-- Worker to translate records
```


## Infrastrcuture and Build Process
### Overview
The bot is deployed within production GCP infrastructure and protected as well as managed via IaC in SpaceLift. Further details are not available here for obvious reasons. If you are an internal employee of Shift Cyber, reach out to the development channels for more information.

### Install
To setup the bot locally you will need to set the approperiate environment variables. This requires SendGrid as well as specific database configuration. For that reason, please reach out to the development team if you would like to get setup with a testing account--they can help you out. :)


## GAR Authentication and Build Process
1. Authenticate to docker<br>
```gcloud auth login```

2. Configure auth for docker (config file)<br>
```gcloud auth configure-docker us-central1-docker.pkg.dev```

3. Verify authentication by pulling your secret<br>
```echo "https://us-central1-docker.pkg.dev" | docker-credential-gcr get```

*You may get an error like "credentials not found in native keychain", this appears to be okay.*

4. Build the image locally<br>
```docker build . -t bits```

5. Tag the local image<br>
```docker tag bits us-central1-docker.pkg.dev/hackabit-sandbox-playhouse/bits/bits:<version>```

*Ensure that your image tag conforms to the vX.X.X naming convention for versioning.*

6. Push it to the artifacts repository<br>
```docker push us-central1-docker.pkg.dev/hackabit-sandbox-playhouse/bits/bits:<version>```


## Environment Variables
Retrieve these secrets from the OnePassword engineering vault: Bits Bot (Environment Settings)

| Environment Variable | Description                           | Required | Default    |
| -------------------- | ------------------------------------- | -------- | ---------- |
| DB_HOST              | Database host address                 | Yes      |            |
| DB_PASS              | Database password                     | Yes      |            |
| DISCORD_TOKEN        | Bot's discord access token            | Yes      |            |
| VERSION              | Version to present in the server      | Yes      |            |
| SENDGRID_API_KEY     | Sendgrid API access key               | Yes      |            |
| SENDGRID_REG         | Sendgride registration email template | Yes      |            |
| TOKEN_EXP_SEC        | Token expiration window in seconds    | Yes      |            |
| DB_USER              | Database user                         | No       | root       |
| DB_NAME              | Database name                         | No       | hack_a_bit |
| LOG_LOCAL            | Integer 1/0 specifing log destination | No       | 0          |

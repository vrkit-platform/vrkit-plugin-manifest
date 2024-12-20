# Welcome to VRKit plugins repository

> Mega thanks goes to the [Flow Launcher](https://github.com/Flow-Launcher/Flow.Launcher) 
> team who have implemented a clear coherent plugin methodology & management system from 
> which the VRKit Plugin Repository was literally cloned (small modifications).

This repository contains the information for community-made plugins used in  and how to make new submissions.

[![AutoUpdate](https://github.com/vrkit-platform/vrkit-plugin-manifest/actions/workflows/updater.yaml/badge.svg?branch=master)](https://github.com/vrkit-platform/vrkit-plugin-manifest/actions/workflows/updater.yaml)

## Plugin list

Looking for a list of currently available plugins in VRKit? Visit [coming soon](#)

## How to submit your plugin

1. Create a file named `${name}-${uuid}.json` in the _plugins_ directory.
2. Copy these items from your plugin project's plugin.json file:
   - `id`
   - `name`
   - `author`
   - `version`
   - `overview`
      - `featureContent`
      - `changeLogContent`
      - `screenshots`
      - `websiteUrl`
      - `iconUrl`
      - `downloadUrl`
      - `sourceUrl`
   - `components` (optional) 
      - if included, a preview of your components & respective screenshots will be visible in the _plugin browser_.

3. It should look like this:
   ```json
   {
    "id": "858a6138-0854-476b-92c1-f1da4a37a48d",
    "version": "1.0.0",
    "name": "VRKit Leaderboard",
    "author": {
        "company": "3FV",
        "name": "Jonathan Glanz",
        "email": "support@3form.ventures"
    },
    "overview": {
        "featureContent": "A real time, configurable leaderboard overlay",
        "changeLogContent": "v1.0.0\n- initial release",
        "screenshots": [],
        "websiteUrl": "https://github.com/vrkit-platform/vrkit-plugin-leaderboard",
        "iconUrl": "https://cdn.jsdelivr.net/gh/vrkit-platform/vrkit-plugin-leaderboard@main/assets/icon.png?raw=true",
        "sourceUrl": "https://github.com/vrkit-platform/vrkit-plugin-leaderboard",
        "downloadUrl": "https://github.com/vrkit-platform/vrkit-plugin-leaderboard/releases/download/v1.0.0/vrkit-plugin-leaderboard.zip",
    },
    "components": [ ... ]
   }
   ```
5. For `iconUrl`, use a CDN provider for global accessibility. [jsdelivr.com](https://www.jsdelivr.com/) for example as shown above, works well with GitHub repositories.
6. It is a requirement to set up a GitHub Actions workflow for automated build and release. Follow the guide [coming soon](#) and use [coming soon](#) as an example.
7. It is a requirement that your plugin conforms with the [Plugin Store policy](#plugin-store-policy).
8. Submit a pull request.
9. The plugin will be available in VRKit after the pull request is approved by the VRKit Team.

VRKit downloads the manifest (plugins.json) file from various CDN providers, which means the availability of your new plugin depends on when these providers sync their updated files. This syncing process can take several days and sometimes up to a week across all providers. During this period, you may see intermittent updates for your plugin in the manifest, as the provider chosen for retrieval is selected randomly based on the fastest fetch speed.

## Plugin updates

Every three hours the *CI* in this repository will check for new updates from plugins and automatically update them to the latest version.

## Plugin Store policy

Plugins that facilitate or contain any of the following will not be allowed:
- Malicious code
- Piracy
- Deceptive use
- Inappropriate content
- Illegal activities
- Impersonation
- Abuse
- Fraud
- Spam

## Plugin Store

Users will be able to install your plugin via the `Plugins` section in the app



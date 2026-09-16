<p align="center">
  <img src="./assets/profile-header.svg" width="100%" alt="The Data Forge — Hrithik028, analytics, engineering, and practical systems" />
</p>

<p align="center">
  <em>“From raw data, useful systems. From complex problems, clear decisions.”</em>
</p>

<p align="center">
  <img src="./assets/data-forge-command-throne.jpeg" width="100%" alt="A blue armored warrior approaching a gothic command throne surrounded by computer terminals" />
</p>

<p align="center">
  <img src="./assets/profile-console.svg" width="100%" alt="Hrithik's Data Forge profile console with biography, featured projects, technical disciplines, and working principles" />
</p>

<details>
<summary><strong>Accessible text dossier</strong></summary>

I’m **Hrithik**, a data-focused builder working across analytics, software, and practical automation. I turn messy data and business questions into clear insights, useful dashboards, and maintainable software products. My path sits between **Data Analyst**, **Analytics Engineer**, and **Full-Stack Developer**.

- **WorkflowHQ:** Full-stack workflow platform built with React, Express, PostgreSQL, and REST APIs.
- **Breaking Games:** SQL and Python analysis across marketing, Shopify, product performance, and customer behaviour.
- **Engineering OS:** Living technical profile documenting projects, contribution activity, and technical growth.
- **Working principle:** Validate the data before trusting the conclusion.

</details>

<p align="center">
  <img src="./assets/sentinel-patrol-line.svg" width="100%" alt="A miniature blue armored marine and green ork exchanging sword strikes along a glowing patrol line" />
</p>

<p align="center">
  <img src="./assets/transmission-header.svg" width="100%" alt="Transmission channels" />
</p>

<p align="center">
  <a href="https://github.com/Hrithik028"><img src="https://img.shields.io/badge/GitHub-Hrithik028-07152d?style=for-the-badge&logo=github&logoColor=d7b35c&labelColor=02050b" alt="Hrithik028 on GitHub" /></a>
  <a href="https://www.linkedin.com/in/hrithik-jadhav-a08068199/"><img src="https://img.shields.io/badge/LinkedIn-Connect-123e8f?style=for-the-badge&logo=linkedin&logoColor=f4ead5&labelColor=02050b" alt="Connect with Hrithik on LinkedIn" /></a>
  <a href="mailto:hrithik.jadhav028@gmail.com"><img src="https://img.shields.io/badge/Email-Transmit-8b1e2d?style=for-the-badge&logo=gmail&logoColor=f4ead5&labelColor=02050b" alt="Email Hrithik" /></a>
</p>

<p align="center">
  <img src="./assets/tech-stack.svg" width="100%" alt="Hrithik's technology stack" />
</p>

<p align="center">
  <img src="./assets/github-stats.svg" width="100%" alt="Verified GitHub statistics snapshot for Hrithik028" />
</p>

<p align="center">
  <img src="./assets/profile-footer.svg" width="100%" alt="The Data Forge endures — built with curiosity, tested with evidence, documented for the next traveller" />
</p>

<details>
<summary><strong>How the GitHub telemetry panel is maintained</strong></summary>

```mermaid
flowchart LR
    T["Sunday schedule or<br/>manual workflow run"] --> A["GitHub Actions"]
    A --> P["scripts/update_profile_stats.py"]
    API["GitHub REST and<br/>GraphQL APIs"] --> P
    P --> SVG["assets/github-stats.svg"]
    SVG --> R["profile README"]
```

The workflow in `.github/workflows/update-profile-stats.yml` is scheduled for `21:17 UTC` each Sunday and also supports manual dispatch. It runs the standard-library Python script with GitHub's repository token, then commits only `assets/github-stats.svg` when that file changes.

Run the generator locally with Python 3:

```powershell
$env:GITHUB_TOKEN = "your_token"
python scripts/update_profile_stats.py
Remove-Item Env:GITHUB_TOKEN
```

`GH_TOKEN` is accepted as an alternative, and `PROFILE_USERNAME` can override the default `Hrithik028` account. Keep credentials in environment variables; never write a token into the repository.

The panel reports a point-in-time count of public repositories, contributions in GitHub's current contribution window, followers, following, and the four most common primary languages among up to 100 owner repositories. Counts can become stale between runs, and API availability, permissions, rate limits, workflow settings, or branch protection can prevent an update. The workflow configuration was reviewed locally; no claim is made here about its latest remote run.

</details>

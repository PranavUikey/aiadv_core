# AIAdventures – Inactive Student Re-engagement Automation

![Inactive Student Agent](https://github.com/PranavUikey/aiadv_core/actions/workflows/inactive_student_mail.yml/badge.svg)

> ⚠️ **Internal Use Only**  
> This repository is intended for internal AIAdventures operations.  
> Not for public or external distribution.

---

## Overview

This system automatically identifies inactive students on the AIAdventures Moodle platform and sends personalized reminder emails to help them resume and complete their courses.

The automation runs **daily via GitHub Actions**, requires **no servers or GPUs**, and follows safe email-sending and deduplication practices.

---

## Key Capabilities

- Detect students inactive for **n days**
- Identify courses with ** almost near completion**
- Generate personalized HTML emails
- AIAdventures branding and logo included
- Duplicate email prevention (cooldown-based)
- Reliable SMTP delivery (Hostinger-tuned)
- Fully automated via GitHub Actions
- Failure detection with alerts

---

## Repository Structure

  aiadv_core/
  ├── analytics/
  
  ├── moodle/
  
  ├── mail/
  
  │ └── email.txt
  
  ├── assets/
  
  │ └── aiadventures_logo.png
  
  
  ├── mailer.py
  
  ├── config.py
  
  ├── main.py


## Ownership

AIAdventures – Training & Operations Team
📧 support@aiadventures.in


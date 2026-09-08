# Рабочие материалы

## Меню и КБЖУ для нутрициолога Юлии

Пакет ТЗ, выбор ИИ и бизнес-план:

- [`docs/yulia-racion-studio/README.md`](docs/yulia-racion-studio/README.md)
- ТЗ: [`docs/yulia-racion-studio/TZ-racion-studio.md`](docs/yulia-racion-studio/TZ-racion-studio.md)
- Эталон меню: [`docs/yulia-racion-studio/preview-menu.html`](docs/yulia-racion-studio/preview-menu.html)

Разбор анкеты практики: [`razbor-ankety-boyarkova-yuliya.md`](razbor-ankety-boyarkova-yuliya.md)

---

# OpenClaw remote backup (Windows)

PowerShell scripts that stream `/home/openclaw` from `194.156.117.210` over SSH into `D:\Backups\server_<date>.tar.gz` and schedule a weekly run.

## Files

| File | Purpose |
|------|---------|
| `backup.ps1` | Backup script (install to `D:\backup.ps1`) |
| `Install-BackupTask.ps1` | Copies script to `D:\` and registers Task Scheduler |

## One-time setup (on the Windows PC)

1. Copy this folder to the PC (or clone the repo).
2. Ensure OpenSSH Client is installed and key-based login works:

```powershell
ssh root@194.156.117.210
```

3. Run elevated PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\Install-BackupTask.ps1
```

Optional: different SSH user:

```powershell
.\Install-BackupTask.ps1 -SshUser openclaw
```

## What gets created

- `D:\backup.ps1`
- `D:\Backups\` (archives + logs)
- Scheduled Task **OpenClaw Server Backup** — every Sunday at **03:00**

## Manual test

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File D:\backup.ps1
```

Archive path: `D:\Backups\server_yyyy-MM-dd.tar.gz`

# mutt_setup

Configures the mutt email client for `sbates@raithlin.com` and
`sbates130272@gmail.com` using OAuth2 tokens.

## Shell environment

Writes `~/.bashrc.d/mutt.sh` with `EMAIL` and `MAIL` exports. This requires
the dotfiles `~/.bashrc.d/` extension point (available since batesste-dotfiles
v3.x).

## Git send-email

Writes `~/.gitconfig.local` with a `[sendemail]` block pointing at
`~/.mutt/scripts/git-sendmail.sh`. If `files/git-sendmail.sh` exists in this
role, it is deployed; otherwise the config is written and the script must be
provided by other means (e.g. dotfiles).

## Variables

| Variable | Default | Description |
|---|---|---|
| `mutt_setup_cache_base` | `.mutt` | Base directory under `~` for mutt state |
| `mutt_setup_google_oauth2_client_secret` | vault | Google OAuth2 client secret |

## Token files

Place OAuth2 token files alongside the role in `files/` before running:

- `sbates@raithlin.com.token`
- `sbates130272@gmail.com.token`

The role skips copying a token if the source file is absent.

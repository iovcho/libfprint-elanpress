# libfprint elanpress for Fedora

RPM build of [filip-rs/libfprint](https://github.com/filip-rs/libfprint) branch `elanpress` for the ELAN `04f3:0c6e` press sensor. The distribution `libfprint` treats that sensor as a swipe reader, and identification fails with `The driver encountered a protocol error with the device`.

The package is pinned to commit `fa2f98fb8cb56e72d9e316cd86a987456b137893`. Its name is `libfprint` and its epoch is 1, so `dnf upgrade` does not replace it with Fedora's newer upstream version.

## Install

Fedora 44, x86_64:

```bash
sudo dnf install -y https://github.com/iovcho/libfprint-elanpress/releases/download/fc44/libfprint-elanpress.fc44.x86_64.rpm
sudo systemctl restart fprintd
fprintd-list "$USER"
```

The device name should be `ElanTech press-type fingerprint sensor`.

To receive later builds from this repository:

```bash
sudo dnf config-manager --add-repo https://raw.githubusercontent.com/iovcho/libfprint-elanpress/main/libfprint-elanpress.repo
sudo dnf upgrade libfprint
```

The packages are not signed (`gpgcheck=0`).

Fingerprints enrolled with Fedora's driver do not work with `elanpress`. Enroll again:

```bash
fprintd-enroll -f right-index-finger
```

Prints enrolled with this same `elanpress` commit stay in place across reinstalls of this package. KDE can also enroll from System Settings → Users (`kcmshell6 kcm_users`).

## Return to Fedora's libfprint

```bash
sudo rm -f /etc/yum.repos.d/libfprint-elanpress.repo
sudo dnf remove libfprint
sudo dnf install libfprint
```

## Build

GitHub Actions builds the RPM on a standard runner in a `fedora:44` container. Standard GitHub-hosted runners are free for this public repository. The workflow publishes the RPM on the `fc44` release and refreshes the `repo` branch used by `dnf`.

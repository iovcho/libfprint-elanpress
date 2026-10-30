# libfprint elanpress for Fedora

RPM build of [filip-rs/libfprint](https://github.com/filip-rs/libfprint) branch `elanpress` for the ELAN `04f3:0c6e` press sensor. Fedora's `libfprint` treats that sensor as a swipe reader, and identification fails with `The driver encountered a protocol error with the device`.

The package name is `libfprint` and the epoch is `1`. With this repository enabled, `dnf` keeps it in place of Fedora's build. The repository is Fedora 44, x86_64 only.

Once an hour the workflow reads `elanpress`. A new commit is published as a new RPM. Older RPMs stay in the repository, so `dnf downgrade` can select one. The release is `2.<commit time>git<short sha>`, so a later `elanpress` commit sorts newer.

The packages are not signed. `gpgcheck=0` is set for that reason. Fedora's own repositories sign their packages and set `gpgcheck=1`.

## Add the repository

```bash
sudo dnf config-manager addrepo --from-repofile=https://raw.githubusercontent.com/iovcho/libfprint-elanpress/main/libfprint-elanpress.repo
```

`dnf` writes `/etc/yum.repos.d/libfprint-elanpress.repo`. Check it with:

```bash
dnf repolist libfprint-elanpress
```

A new build can take about an hour to appear, plus a few minutes of cache on `raw.githubusercontent.com`. `dnf upgrade --refresh` asks for fresh metadata.

## Install or upgrade

```bash
sudo dnf upgrade --refresh libfprint
sudo systemctl restart fprintd
fprintd-list "$USER"
```

The device name should be `ElanTech press-type fingerprint sensor`.

`dnf` reports that OpenPGP checks were skipped for this repository. That matches `gpgcheck=0`.

Fingerprints enrolled with Fedora's driver do not work with `elanpress`. Enroll again:

```bash
fprintd-enroll -f right-index-finger
```

Prints enrolled with this `elanpress` driver stay in place when a later build of this package is installed. KDE can also enroll from System Settings → Users (`kcmshell6 kcm_users`).

A single RPM from the `fc44` release installs the latest build and does not add this repository, so later upgrades and downgrades are not available until the repository file is installed:

```bash
sudo dnf install -y https://github.com/iovcho/libfprint-elanpress/releases/download/fc44/libfprint-elanpress.fc44.x86_64.rpm
```

## Downgrade

Every published build stays in the repository. List them and move to the newest older build:

```bash
dnf list --showduplicates libfprint
sudo dnf downgrade libfprint
sudo systemctl restart fprintd
```

To select one build, pass its name, epoch, version, and release. `dnf list --showduplicates libfprint` prints that string:

```bash
sudo dnf downgrade libfprint-1:1.94.10-<release>.fc44
```

Downgrade stays inside this repository. It does not install Fedora's `libfprint`, because that package has epoch `0`.

## Return to Fedora's libfprint

Disable the repository, then sync the package to the version in Fedora's repositories. `dnf distro-sync` downgrades `libfprint` without removing `fprintd`:

```bash
sudo rm -f /etc/yum.repos.d/libfprint-elanpress.repo
sudo dnf distro-sync libfprint
sudo systemctl restart fprintd
```

Confirm the package comes from `fedora` or `updates`:

```bash
dnf list --installed libfprint
```

Fingerprints enrolled with `elanpress` do not work with Fedora's driver. Enroll again after the switch.

## Build

GitHub Actions checks `elanpress` every hour (`17 * * * *`). A new commit starts a build in a `fedora:44` container on a standard runner. The RPM is added to the `fc44` release and to the `repo` branch used by `dnf`. Older RPMs are left in place. An unchanged commit does not rebuild. A push to this repository builds the current `elanpress` commit even when it was built before.

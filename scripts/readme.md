## Packaging

Add-on is packaged as a simple ZIP file.

### Prerequisites

Add executable permissions to `package.sh`

```
chmod +x package.sh
```

Before packaging the add-on make sure you have all changes in GIT:

```
git add .
git commit -m "YOUR MESSAGE"
```

### Run

From root folder:

```
./scripts/package.sh
```

ZIP file will be put into `./output` folder.


let dryRun = (process.env.RELEASE_DRY_RUN || "false").toLowerCase() === "true";
let testPypi = (process.env.RELEASE_TEST_PYPI || "false").toLowerCase() === "true";
const pypiToken = process.env.PYPI_TOKEN;
const testPypiToken = process.env.TEST_PYPI_TOKEN;

// Publishing to (Test)PyPI happens in `prepare`, i.e. before @semantic-release/git commits and
// before the tag is pushed: if the upload fails, no release commit or tag is produced.
let publishCmd = `uv publish --token `;

if (testPypi) {
    publishCmd += `${testPypiToken} --index testpypi`;
} else {
    publishCmd += `${pypiToken}`;
}

if (dryRun) {
    publishCmd += " --dry-run";
}

// Fail in verifyConditions, before anything is built, if the token for the target index is missing.
const tokenVar = testPypi ? "TEST_PYPI_TOKEN" : "PYPI_TOKEN";
const verifyConditionsCmd = dryRun
    ? undefined
    : `test -n "$${tokenVar}" || { echo "${tokenVar} is not set" >&2; exit 1; }`;

// The Docker image (see Dockerfile), for amd64 and arm64, on GitHub Packages: tagged with the version
// and `latest`. Built in `prepare`, before publishing on PyPI (so that a failing build stops the
// release), and pushed in `publish`, once the release is tagged (the build is cached by then).
const image = `ghcr.io/${(process.env.GITHUB_REPOSITORY || "tuprolog/2ppy").toLowerCase()}`;
const dockerBuildCmd = "docker buildx build --platform linux/amd64,linux/arm64"
    + ` --tag ${image}:\${nextRelease.version} --tag ${image}:latest .`;

// dist/ is emptied first, as the image installs every wheel there
const prepareCmd = `rm -rf dist && uv version \${nextRelease.version} && uv build && ${dockerBuildCmd} && ${publishCmd}`;
const dockerPublishCmd = `${dockerBuildCmd} --push`;

import config from 'semantic-release-preconfigured-conventional-commits' with {type: 'json'};

config.plugins.push(
    ["@semantic-release/exec", {
        "verifyConditionsCmd": verifyConditionsCmd,
        "prepareCmd": prepareCmd,
        "publishCmd": dockerPublishCmd,
    }]
)

if (!dryRun) {
    config.plugins.push(
        ["@semantic-release/github", {
            "assets": [
                // Not dist/*: `uv build` also writes dist/.gitignore, which would be uploaded.
                { "path": "dist/*.whl" },
                { "path": "dist/*.tar.gz" },
            ]
        }],
        ["@semantic-release/git", {
            "assets": [
                "CHANGELOG.md",
                "pyproject.toml",
                "uv.lock"
            ],
            "message": "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}"
        }]
    );
}

// semantic-release itself must not tag or push either, when dry-running
config.dryRun = dryRun;

export default config;
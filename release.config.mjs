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

const prepareCmd = `uv version \${nextRelease.version} && uv build && ${publishCmd}`;

import config from 'semantic-release-preconfigured-conventional-commits' with {type: 'json'};

config.plugins.push(
    ["@semantic-release/exec", {
        "verifyConditionsCmd": verifyConditionsCmd,
        "prepareCmd": prepareCmd,
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

export default config;
#!/usr/bin/env node
/**
 * Auto-allow safe git ops; deny force-push / config / secret-touching commands.
 * Input: JSON on stdin from beforeShellExecution.
 */
const fs = require("fs");

function readStdin() {
  try {
    return fs.readFileSync(0, "utf8");
  } catch {
    return "";
  }
}

function respond(obj) {
  process.stdout.write(JSON.stringify(obj));
  process.exit(0);
}

const raw = readStdin();
let payload = {};
try {
  payload = JSON.parse(raw || "{}");
} catch {
  respond({ permission: "ask" });
}

const command = String(payload.command || "");
const lower = command.toLowerCase();

const denyPatterns = [
  /git\s+push\s+.*--force/,
  /git\s+push\s+.*-f\b/,
  /git\s+push\s+.*--force-with-lease/,
  /git\s+reset\s+--hard/,
  /git\s+clean\s+-[a-z]*f/,
  /git\s+config\b/,
  /\.env\b/,
  /credentials\.json/,
  /id_rsa/,
  /secrets?[\\/]/,
];

for (const re of denyPatterns) {
  if (re.test(lower)) {
    respond({
      permission: "deny",
      user_message:
        "Comando git bloqueado pelo hook Omega (force push, git config ou secrets).",
      agent_message:
        "Hook negou o comando: force push, git config ou possível vazamento de secrets não são permitidos.",
    });
  }
}

const allowPrefixes = [
  "git status",
  "git diff",
  "git log",
  "git show",
  "git add",
  "git commit",
  "git push",
  "git fetch",
  "git pull",
  "git branch",
  "git rev-parse",
  "git remote",
  "git ls-files",
  "git ls-remote",
  "git tag",
  "git describe",
  "git symbolic-ref",
  "git merge-base",
  "git stash",
];

const trimmed = command.trim().replace(/^["']|["']$/g, "");
// PowerShell often wraps: git status; ... — allow if the primary segment is safe git
const primary = trimmed.split(/[;&\n]/)[0].trim();
const primaryLower = primary.toLowerCase();

const isAllowed = allowPrefixes.some(
  (p) => primaryLower === p || primaryLower.startsWith(p + " ")
);

if (isAllowed || /^git\s/.test(primaryLower) && allowPrefixes.some((p) => primaryLower.startsWith(p))) {
  respond({ permission: "allow" });
}

// Non-matching git / other: leave to Cursor default policy
respond({ permission: "ask" });

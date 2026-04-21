module.exports = {
  apps: [
    {
      name: "muhendisal-api",
      script: "/root/muhendisal-platform/venv/bin/uvicorn",
      args: "backend.main:app --host 127.0.0.1 --port 9100",
      cwd: "/root/muhendisal-platform",
      interpreter: "none",
      autorestart: true,
      watch: false,
      max_memory_restart: "300M",
      env: {
        PYTHONUNBUFFERED: "1"
      },
      out_file: "/var/log/pm2-muhendisal-api.log",
      error_file: "/var/log/pm2-muhendisal-api-err.log",
      merge_logs: true,
      time: true
    }
  ]
};

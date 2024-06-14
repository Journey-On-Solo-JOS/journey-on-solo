module.exports = {
  apps: [
    {
      name: 'fastapi',
      script: 'uvicorn main:app --host 0.0.0.0 --port 3000',
      env: {
        PORT: 3000,
        ENVIRONMENT: 'venv',
      },
    },
  ],
};

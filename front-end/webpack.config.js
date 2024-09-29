const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const dotenv = require("dotenv");
const fs = require("fs");
const webpack = require("webpack");

// Function to find .env file in current or parent directories
function findEnvFile(startPath) {
  let currentPath = startPath;
  while (currentPath !== path.parse(currentPath).root) {
    const envPath = path.join(currentPath, ".env");
    if (fs.existsSync(envPath)) {
      return envPath;
    }
    currentPath = path.dirname(currentPath);
  }
  return null;
}

// Find and load .env file
const envPath = findEnvFile(__dirname);
let env = {};
if (envPath) {
  console.log(`Loading .env file from: ${envPath}`);
  env = dotenv.config({ path: envPath }).parsed;
} else {
  console.warn("No .env file found in parent directories");
}

// Create a new object with only REACT_APP_ variables
const processEnv = Object.keys(env)
  .filter(key => key.startsWith('REACT_APP_'))
  .reduce((obj, key) => {
    obj[key] = JSON.stringify(env[key]);
    return obj;
  }, {});

// Add NODE_ENV and other necessary variables
processEnv['NODE_ENV'] = JSON.stringify(process.env.NODE_ENV || 'development');

module.exports = {
  entry: "./src/index.tsx",
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "bundle.js",
  },
  resolve: {
    extensions: [".ts", ".tsx", ".js", ".jsx"],
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: [
          {
            loader: "ts-loader",
            options: {
              transpileOnly: true,
            },
          },
        ],
        exclude: /node_modules/,
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: "./src/index.html",
    }),
    new webpack.DefinePlugin({
      'process.env': processEnv
    }),
  ],
  devServer: {
    static: path.join(__dirname, 'dist'),
    allowedHosts: 'all',
    compress: true,
    port: process.env.FRONT_PORT || 3010,
    headers: {
      'Cache-Control': 'no-store',
    },
  },
  devtool: "inline-source-map",
};

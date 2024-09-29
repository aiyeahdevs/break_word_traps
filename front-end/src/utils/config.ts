import * as dotenv from "dotenv";

export const config = {
  backendUrl: `${process.env.REACT_APP_BACK_URL}`,
};

console.log(config.backendUrl);

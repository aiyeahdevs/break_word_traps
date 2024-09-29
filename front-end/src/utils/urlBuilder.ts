import { config } from "./config";

export function buildUrl(path: string) {
  // join paths
  return `${config.backendUrl}/${path}`;
}

import { Job } from '../types';

const DATA_URL = import.meta.env.VITE_DATA_URL || '/data/jobs.json';

export async function fetchJobs(): Promise<Job[]> {
  const timestamp = Date.now();
  const url = `${DATA_URL}?t=${timestamp}`;
  
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch jobs:', error);
    return [];
  }
}

export function startPolling(callback: (jobs: Job[]) => void): () => void {
  const poll = async () => {
    const jobs = await fetchJobs();
    callback(jobs);
  };
  
  // Initial fetch
  poll();
  
  // Poll every 30 minutes
  const interval = setInterval(poll, 30 * 60 * 1000);
  
  return () => clearInterval(interval);
}
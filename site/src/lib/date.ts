export function parseDate(dateStr: string): Date {
  if (!dateStr) return new Date(0);
  const date = new Date(dateStr);
  return isNaN(date.getTime()) ? new Date(0) : date;
}

export function formatRelativeTime(dateStr: string): string {
  const date = parseDate(dateStr);
  if (date.getTime() === 0) return 'Unknown';
  
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  
  if (diffDays === 0) return 'Today';
  if (diffDays === 1) return '1 day ago';
  return `${diffDays} days ago`;
}

export function isWithinDays(dateStr: string, days: number): boolean {
  const date = parseDate(dateStr);
  if (date.getTime() === 0) return false;
  
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffDays = diffMs / (1000 * 60 * 60 * 24);
  
  return diffDays <= days;
}
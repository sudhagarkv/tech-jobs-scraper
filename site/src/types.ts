export interface Job {
  company: string;
  title: string;
  location: string;
  url: string;
  posted_date: string;
  provider: string;
  description: string;
  role_category: string;
  level: string;
}

export interface Filters {
  roleCategories: string[];
  levels: string[];
  remoteOnly: boolean;
  location: string;
  postedWithin: string;
  search: string;
}
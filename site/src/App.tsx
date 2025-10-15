import { useState, useEffect, useMemo } from 'react';
import { Job, Filters } from './types';
import { FiltersComponent } from './components/Filters';
import { JobsTable } from './components/JobsTable';
import { startPolling } from './lib/fetchData';
import { parseDate, isWithinDays } from './lib/date';

function App() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<Filters>({
    roleCategories: [],
    levels: [],
    remoteOnly: false,
    location: '',
    postedWithin: 'all',
    search: '',
  });

  useEffect(() => {
    const stopPolling = startPolling((fetchedJobs) => {
      setJobs(fetchedJobs);
      setLoading(false);
    });

    return stopPolling;
  }, []);

  const filteredJobs = useMemo(() => {
    return jobs.filter(job => {
      // Remote only filter
      if (filters.remoteOnly && !job.location.toLowerCase().includes('remote')) {
        return false;
      }

      // Location filter
      if (filters.location && !job.location.toLowerCase().includes(filters.location.toLowerCase())) {
        return false;
      }

      // Posted within filter
      if (filters.postedWithin !== 'all') {
        const days = parseInt(filters.postedWithin);
        if (!isWithinDays(job.posted_date, days)) {
          return false;
        }
      }

      // Search filter
      if (filters.search) {
        const searchLower = filters.search.toLowerCase();
        const matchesCompany = job.company.toLowerCase().includes(searchLower);
        const matchesTitle = job.title.toLowerCase().includes(searchLower);
        if (!matchesCompany && !matchesTitle) {
          return false;
        }
      }

      return true;
    });
  }, [jobs, filters]);

  const lastUpdated = useMemo(() => {
    if (jobs.length === 0) return null;
    
    const dates = jobs
      .map(job => parseDate(job.posted_date))
      .filter(date => date.getTime() > 0)
      .sort((a, b) => b.getTime() - a.getTime());
    
    return dates.length > 0 ? dates[0] : null;
  }, [jobs]);

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">
              US Entry-Level & New-Grad Tech Roles
            </h1>
            <div className="text-sm text-gray-500">
              {lastUpdated && (
                <div>Last updated: {lastUpdated.toLocaleDateString()}</div>
              )}
              <div>{jobs.length} total jobs</div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          <div className="lg:col-span-1">
            <FiltersComponent filters={filters} onFiltersChange={setFilters} />
          </div>
          
          <div className="lg:col-span-3">
            <div className="mb-4">
              <div className="text-sm text-gray-600">
                Showing {filteredJobs.length} of {jobs.length} jobs
              </div>
            </div>
            <JobsTable jobs={filteredJobs} loading={loading} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
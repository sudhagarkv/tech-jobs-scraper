import { X, Search } from 'lucide-react';
import { Filters } from '../types';

interface FiltersProps {
  filters: Filters;
  onFiltersChange: (filters: Filters) => void;
}


const POSTED_OPTIONS = [
  { value: 'all', label: 'All (3 months)' },
  { value: '7', label: '7 days' },
  { value: '14', label: '14 days' },
  { value: '30', label: '30 days' },
  { value: '60', label: '60 days' },
];

export function FiltersComponent({ filters, onFiltersChange }: FiltersProps) {
  const updateFilters = (updates: Partial<Filters>) => {
    onFiltersChange({ ...filters, ...updates });
  };



  const clearFilters = () => {
    onFiltersChange({
      roleCategories: [],
      levels: [],
      remoteOnly: false,
      location: '',
      postedWithin: 'all',
      search: '',
    });
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">Filters</h2>
        <button
          onClick={clearFilters}
          className="text-sm text-gray-500 hover:text-gray-700 flex items-center gap-1"
        >
          <X className="w-4 h-4" />
          Clear all
        </button>
      </div>



      <div>
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={filters.remoteOnly}
            onChange={(e) => updateFilters({ remoteOnly: e.target.checked })}
            className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
          />
          <span className="text-sm font-medium">Remote only</span>
        </label>
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Location contains</label>
        <input
          type="text"
          value={filters.location}
          onChange={(e) => updateFilters({ location: e.target.value })}
          placeholder="e.g. San Francisco, Remote"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Posted Within</label>
        <select
          value={filters.postedWithin}
          onChange={(e) => updateFilters({ postedWithin: e.target.value })}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          {POSTED_OPTIONS.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Search</label>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <input
            type="text"
            value={filters.search}
            onChange={(e) => updateFilters({ search: e.target.value })}
            placeholder="Company or job title"
            className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>
    </div>
  );
}
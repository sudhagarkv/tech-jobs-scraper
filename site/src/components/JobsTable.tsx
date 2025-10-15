import { useMemo, useState } from 'react';
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getPaginationRowModel,
  createColumnHelper,
  flexRender,
  SortingState,
} from '@tanstack/react-table';
import { ChevronUp, ChevronDown, ExternalLink } from 'lucide-react';
import { Job } from '../types';
import { formatRelativeTime, parseDate } from '../lib/date';

interface JobsTableProps {
  jobs: Job[];
  loading: boolean;
}

const columnHelper = createColumnHelper<Job>();

export function JobsTable({ jobs, loading }: JobsTableProps) {
  const [sorting, setSorting] = useState<SortingState>([
    { id: 'posted_date', desc: true }
  ]);
  const [pageSize, setPageSize] = useState(25);

  const columns = useMemo(() => [
    columnHelper.accessor('company', {
      header: 'Company',
      cell: info => (
        <div className="font-medium text-gray-900">{info.getValue()}</div>
      ),
    }),
    columnHelper.accessor('title', {
      header: 'Title',
      cell: info => (
        <div className="text-gray-900">{info.getValue()}</div>
      ),
    }),
    columnHelper.accessor('role_category', {
      header: 'Role',
      cell: info => (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
          {info.getValue()}
        </span>
      ),
    }),
    columnHelper.accessor('level', {
      header: 'Level',
      cell: info => (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
          {info.getValue()}
        </span>
      ),
    }),
    columnHelper.accessor('location', {
      header: 'Location',
      cell: info => (
        <div className="text-gray-600 text-sm">{info.getValue()}</div>
      ),
    }),
    columnHelper.display({
      id: 'remote',
      header: 'Remote',
      cell: info => (
        <div className="text-center">
          {info.row.original.location.toLowerCase().includes('remote') ? '✓' : '—'}
        </div>
      ),
    }),
    columnHelper.accessor('posted_date', {
      header: 'Posted',
      cell: info => (
        <div className="text-gray-600 text-sm">
          {formatRelativeTime(info.getValue())}
        </div>
      ),
      sortingFn: (rowA, rowB) => {
        const dateA = parseDate(rowA.original.posted_date);
        const dateB = parseDate(rowB.original.posted_date);
        return dateA.getTime() - dateB.getTime();
      },
    }),
    columnHelper.display({
      id: 'apply',
      header: 'Apply',
      cell: info => (
        <a
          href={info.row.original.url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 px-3 py-1 text-sm font-medium text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-md transition-colors"
        >
          Apply
          <ExternalLink className="w-3 h-3" />
        </a>
      ),
    }),
  ], []);

  const table = useReactTable({
    data: jobs,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    initialState: {
      pagination: { pageSize },
    },
  });

  // Update page size when changed
  useMemo(() => {
    table.setPageSize(pageSize);
  }, [pageSize, table]);

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="p-6">
          <div className="animate-pulse space-y-4">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="flex space-x-4">
                <div className="h-4 bg-gray-200 rounded w-1/4"></div>
                <div className="h-4 bg-gray-200 rounded w-1/3"></div>
                <div className="h-4 bg-gray-200 rounded w-1/6"></div>
                <div className="h-4 bg-gray-200 rounded w-1/6"></div>
                <div className="h-4 bg-gray-200 rounded w-1/4"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (jobs.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border p-12 text-center">
        <div className="text-gray-500">
          <div className="text-lg font-medium mb-2">No jobs found</div>
          <div className="text-sm">Try adjusting your filters to see more results.</div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            {table.getHeaderGroups().map(headerGroup => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map(header => (
                  <th
                    key={header.id}
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    {header.isPlaceholder ? null : (
                      <div
                        className={`flex items-center gap-2 ${
                          header.column.getCanSort() ? 'cursor-pointer select-none' : ''
                        }`}
                        onClick={header.column.getToggleSortingHandler()}
                      >
                        {flexRender(header.column.columnDef.header, header.getContext())}
                        {header.column.getCanSort() && (
                          <div className="flex flex-col">
                            <ChevronUp
                              className={`w-3 h-3 ${
                                header.column.getIsSorted() === 'asc' ? 'text-gray-900' : 'text-gray-300'
                              }`}
                            />
                            <ChevronDown
                              className={`w-3 h-3 -mt-1 ${
                                header.column.getIsSorted() === 'desc' ? 'text-gray-900' : 'text-gray-300'
                              }`}
                            />
                          </div>
                        )}
                      </div>
                    )}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {table.getRowModel().rows.map(row => (
              <tr key={row.id} className="hover:bg-gray-50">
                {row.getVisibleCells().map(cell => (
                  <td key={cell.id} className="px-6 py-4 whitespace-nowrap">
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="px-6 py-4 border-t border-gray-200 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-700">Show</span>
            <select
              value={pageSize}
              onChange={(e) => setPageSize(Number(e.target.value))}
              className="border border-gray-300 rounded px-2 py-1 text-sm"
            >
              {[10, 25, 50].map(size => (
                <option key={size} value={size}>{size}</option>
              ))}
            </select>
            <span className="text-sm text-gray-700">per page</span>
          </div>
          <div className="text-sm text-gray-700">
            Showing {table.getState().pagination.pageIndex * pageSize + 1} to{' '}
            {Math.min((table.getState().pagination.pageIndex + 1) * pageSize, jobs.length)} of{' '}
            {jobs.length} results
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => table.previousPage()}
            disabled={!table.getCanPreviousPage()}
            className="px-3 py-1 text-sm border border-gray-300 rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
          >
            Previous
          </button>
          <span className="text-sm text-gray-700">
            Page {table.getState().pagination.pageIndex + 1} of {table.getPageCount()}
          </span>
          <button
            onClick={() => table.nextPage()}
            disabled={!table.getCanNextPage()}
            className="px-3 py-1 text-sm border border-gray-300 rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}
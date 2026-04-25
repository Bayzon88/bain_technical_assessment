import React from "react";
import remarkGfm from "remark-gfm";
import ReactMarkdown from "react-markdown";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { useReportContext } from "@/context/reportContext";

import "@/styles/loader.css"; // make sure you place your loader CSS here

const Reports = () => {
  const { open, setOpen, report } = useReportContext();

  const isLoading = open && !report;

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className='!w-[1500px] !max-w-[1500px] max-h-[80vh] overflow-y-auto'>
        <DialogHeader>
          <DialogTitle>Company Insights Report</DialogTitle>
        </DialogHeader>

        {/* Loading State */}
        {isLoading && (
          <div className='flex justify-center items-center py-10'>
            <div className='loader' />
          </div>
        )}

        {/* Report Content */}
        {!isLoading && report && (
          <div className=' text-sm leading-relaxed max-w-[1500px]'>
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                h1: ({ children }) => (
                  <h1 className='text-xl font-bold mt-6 mb-3 border-b pb-2'>{children}</h1>
                ),
                h2: ({ children }) => (
                  <h2 className='text-lg font-semibold mt-5 mb-2 border-b pb-1'>{children}</h2>
                ),
                h3: ({ children }) => (
                  <h3 className='text-base font-semibold mt-4 mb-1'>{children}</h3>
                ),
                p: ({ children }) => <p className='mb-3'>{children}</p>,
                ul: ({ children }) => (
                  <ul className='list-disc list-outside pl-5 mb-3 space-y-1'>{children}</ul>
                ),
                ol: ({ children }) => (
                  <ol className='list-decimal list-outside pl-5 mb-3 space-y-1'>{children}</ol>
                ),
                li: ({ children }) => <li className='leading-relaxed'>{children}</li>,
                strong: ({ children }) => <strong className='font-semibold'>{children}</strong>,
                a: ({ href, children }) => (
                  <a
                    href={href}
                    target='_blank'
                    rel='noopener noreferrer'
                    className='text-blue-600 underline hover:text-blue-800'
                  >
                    {children}
                  </a>
                ),
                hr: () => <hr className='my-4 border-t border-gray-200' />,
              }}
            >
              {report}
            </ReactMarkdown>
          </div>
        )}

        {/* Empty fallback (optional safety) */}
        {!isLoading && !report && (
          <div className='text-center text-sm text-gray-500 py-10'>No report available.</div>
        )}
      </DialogContent>
    </Dialog>
  );
};

export default Reports;

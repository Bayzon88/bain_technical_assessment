import React, { createContext, useContext, useState } from "react";

type ReportContextType = {
  report: string;
  open: boolean;
  setOpen: (open: boolean) => void;
  generateReport: (companyName: string, approach: string) => Promise<void>;
};

type ReportResponseType = {
  company_name: string;
  message: string;
  report: string;
};

const ReportContext = createContext<ReportContextType | undefined>(undefined);

export const ReportProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [report, setReport] = useState("");
  const [open, setOpen] = useState(false);

  const generateReport = async (companyName: string, approach: string) => {
    setReport("");
    setOpen(true);
    if (!companyName.trim()) {
      setOpen(false);
      alert("Please enter a company name.");
      return;
    }

    try {
      const params = new URLSearchParams({
        company_name: companyName,
        approach: approach || "",
        date_start: "",
        date_end: "",
      });

      // const response = await fetch(`http://127.0.0.1:8000/api/v1/insights/?${params.toString()}`); #Local test
      const response = await fetch(
        `https://alvarobeltran.dev/business-insights-api/api/v1/insights/?${params.toString()}`,
      ); //Production TODO: move to env variable

      if (response.status === 404) {
        setReport(
          "No report found for the given company and approach. Please try a different company.",
        );

        return;
      } else if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to fetch report");
      } else {
        const data: ReportResponseType = await response.json();

        setReport(data.report || "");
        setOpen(true); // 🔥 automatically opens dialog
      }
    } catch (error) {
      console.error("Error fetching report:", error);
      setOpen(false);
    }
  };

  return (
    <ReportContext.Provider value={{ report, open, setOpen, generateReport }}>
      {children}
    </ReportContext.Provider>
  );
};

export const useReportContext = () => {
  const context = useContext(ReportContext);
  if (!context) {
    throw new Error("useReport must be used within ReportProvider");
  }
  return context;
};

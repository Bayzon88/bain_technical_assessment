import { useContext, useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "./assets/vite.svg";
import heroImg from "./assets/hero.png";
import "./App.css";
import { Dialog } from "./components/ui/dialog";

import SearchBar from "./components/search-bar/search-bar";
import ReportDialog from "./components/report/report";
import { ReportProvider, useReportContext } from "./context/reportContext";

function App() {
  return (
    <ReportProvider>
      <SearchBar />
      <ReportDialog />
    </ReportProvider>
  );
}

export default App;

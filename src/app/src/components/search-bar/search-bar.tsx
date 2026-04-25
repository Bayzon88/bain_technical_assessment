import React, { useState } from "react";
import { Field, FieldLabel } from "../ui/field";
import { Input } from "../ui/input";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "../ui/button";
import { useReportContext } from "@/context/reportContext";

const SearchBar = () => {
  const [companyName, setCompanyName] = useState<string>("");
  const [approach, setApproach] = useState<string>("");
  const { generateReport, open, setOpen } = useReportContext();

  const fetchReport = () => {
    generateReport(companyName, approach);
  };
  return (
    <div>
      <div className='flex w-100 justify-content-center gap-4 p-4'>
        <div className='w-100'>
          <Field className='flex w-96'>
            <FieldLabel htmlFor='input-company-name'>Company Name</FieldLabel>
            <Input
              id='input-company-name'
              placeholder='Enter company name'
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
            />
          </Field>
        </div>

        <div>
          <Field className='flex w-50'>
            <FieldLabel>Report approach</FieldLabel>
            {/* TODO: fix unknown type error in select element */}
            <Select onValueChange={(value) => setApproach(value)}>
              <SelectTrigger className='w-full max-w-48'>
                <SelectValue placeholder='Select an approach' />
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  <SelectLabel>Approach</SelectLabel>
                  <SelectItem value='finance'>Finance</SelectItem>
                  <SelectItem value='business'>Business</SelectItem>
                  <SelectItem value='marketing'>Marketing</SelectItem>
                  <SelectItem value='technology'>Technology</SelectItem>
                </SelectGroup>
              </SelectContent>
            </Select>
          </Field>
        </div>
      </div>

      <div className='flex w-156 justify-end gap-4 p-4'>
        <Button onClick={fetchReport}>Generate Report</Button>
      </div>
    </div>
  );
};

export default SearchBar;

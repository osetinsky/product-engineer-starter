"use client";

import "@/styles/components.css";

import { useState } from 'react';
import { useDashboard } from "@/context/dashboard-context";
import { FaCheck, FaSpinner } from "react-icons/fa";
import { toast } from 'react-toastify';
import { simulateUpload } from "@/utils/uploadUtils";
import classNames from "classnames";

export default function GuidelinesUpload() {
    const { guidelinesFile, setGuidelinesFile, medicalRecord } = useDashboard();
    const [isUploading, setIsUploading] = useState(false);

    const DUMMY_GUIDELINES_PATH = "/assets/guidelines.pdf";

    const handleClick = () => {
        // dismiss any toasts visible when user clicked
        // note: this should later be made conditional based on type of toast
        // for now, assume they're error toasts that no longer apply after click
        toast.dismiss();

        if (!medicalRecord || !medicalRecord.url) {
            toast.error("Please upload a Medical Record first.");
            return;
        }

        setIsUploading(true);

        simulateUpload(() => {
            setGuidelinesFile({ url: DUMMY_GUIDELINES_PATH });
            setIsUploading(false);
        });
    };

    let content;

    if (isUploading) {
        content = (
            <div className="flex flex-row gap-1 items-center">
                <FaSpinner className="animate-spin" />
                <span>Uploading...</span>
            </div>
        );
    } else if (guidelinesFile?.url) {
        content = (
            <div className="flex flex-row gap-1 items-center text-green-600">
                <FaCheck className="animate-check" />
                <span>Guidelines File Uploaded</span>
            </div>
        );
    } else {
        content = (
            <button
                className="text-white font-medium py-2 px-4 rounded border border-2 bg-orange-500 border-orange-500"
                onClick={handleClick}
            >
                <span>Simulate Guidelines Upload</span>
            </button>
        );
    }

    return (
        <div className={classNames(
            "w-1/2 h-64 border border-4 border-gray-200 border-dashed",
            "rounded flex flex-row items-center justify-center"
        )}>
            {content}
        </div>
    );
}
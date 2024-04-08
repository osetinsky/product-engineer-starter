"use client";

import "@/styles/components.css";

import { useState } from 'react';
import { useDashboard } from "@/context/dashboard-context";
import { FaCheck, FaSpinner } from "react-icons/fa";
import { toast } from 'react-toastify';
import { simulateUpload } from "@/utils/uploadUtils";
import classNames from "classnames";

export default function MedicalRecordUpload() {
    const { medicalRecord, setMedicalRecord } = useDashboard();
    const [isUploading, setIsUploading] = useState(false);

    const DUMMY_MEDICAL_RECORD_PATH = "/assets/medical-record.pdf";

    const handleClick = () => {
        // dismiss any toasts visible when user clicked
        // note: this should later be made conditional based on type of toast
        // for now, assume they're error toasts that no longer apply after click
        toast.dismiss();

        setIsUploading(true);
        simulateUpload(() => {
            setMedicalRecord({ url: DUMMY_MEDICAL_RECORD_PATH });
            setIsUploading(false);

            // dismiss any toasts triggered after upload started
            toast.dismiss();
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
    } else if (medicalRecord?.url) {
        content = (
            <div className="flex flex-row gap-1 items-center text-green-600">
                <FaCheck className="animate-check" />
                <span>Medical Record Uploaded</span>
            </div>
        );
    } else {
        content = (
            <button
                className="text-white font-medium py-2 px-4 rounded border border-2 bg-blue-500 border-blue-500"
                onClick={handleClick}
            >
                <span>Simulate Medical Record Upload</span>
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

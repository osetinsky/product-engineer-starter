"use client";

import GuidelinesUpload from "@/components/guidelines-upload";
import MedicalRecordUpload from "@/components/medical-record-upload";
import { useDashboard } from "@/context/dashboard-context";
import { useRouter } from "next/navigation";
import { serverUrl } from '@/utils/config';

import classNames from "classnames";

export const revalidate = 0;

export default function DashboardRoot() {
    const router = useRouter();
    const { medicalRecord, guidelinesFile } = useDashboard();

    const handleContinue = async () => {
        if (bothFilesUploaded) {
            // Next step is to either use formData or encoding to pass uploaded PDFs for medicalRecord and guidelinesFile
            try {
                const response = await fetch(`${serverUrl}/cases`, {
                    mode: 'cors', // Specify CORS mode for request to server
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    router.push(`/dashboard/case/${data.case_id}`);
                } else {
                    console.error('Failed to create case:', response.statusText);
                }
            } catch (error) {
                console.error('Network error:', error);
            }
        }
    };

    const bothFilesUploaded = medicalRecord?.url && guidelinesFile?.url;

    return (
        <div className="w-full flex flex-col justify-center items-center h-screen">
            <div className="w-full flex flex-row gap-2 items-center">
                <MedicalRecordUpload />
                <GuidelinesUpload />
            </div>
            <div className="w-full py-4 flex flex-row justify-center">
                <button
                    className={classNames(
                        "font-medium py-2 px-4 rounded transition-opacity duration-300",
                        {
                            "bg-green-600 text-white": bothFilesUploaded,
                            "bg-transparent text-transparent pointer-events-none": !bothFilesUploaded,
                        }
                    )}
                    onClick={handleContinue}
                    disabled={!bothFilesUploaded}
                >
                    Continue
                </button>
            </div>
        </div>
    );
}
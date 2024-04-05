const DEFAULT_DUMMY_UPLOAD_DELAY = 3000;

export const simulateUpload = (onSuccess: () => void, delay: number = DEFAULT_DUMMY_UPLOAD_DELAY) => {
    setTimeout(() => {
        onSuccess();
    }, delay);
};
const isProduction = process.env.NEXT_PUBLIC_NODE_ENV === 'production';
const protocol = isProduction ? 'https' : 'http';
export const serverUrl = `${protocol}://${process.env.NEXT_PUBLIC_SERVER_HOST}:${process.env.NEXT_PUBLIC_SERVER_PORT}`;

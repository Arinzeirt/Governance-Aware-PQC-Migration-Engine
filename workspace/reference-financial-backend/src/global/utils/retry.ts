export const functionRetry = async (
  sendFn: () => Promise<any>,
  retries = 3,
  delayMs = 1000,
): Promise<any> => {
  try {
    return await sendFn();
  } catch (error) {
    if (retries <= 0) {
      throw error;
    }

    console.warn(`Retrying in ${delayMs}ms... (${retries} left)`);

    await new Promise((res) => setTimeout(res, delayMs));
    return functionRetry(sendFn, retries - 1, delayMs * 2);
  }
};

export const formatDate = (date) => {
  // Return an empty string for null, undefined, or empty inputs
  if (!date) {
    return "NO DATE";
  }

  const dateObject = new Date(date);

  // Check if the created date is valid
  if (isNaN(dateObject.getTime())) {
    return "INVALID DATE"; // Or a placeholder like 'Invalid Date'
  }

  const options = {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    timeZone: 'IST', //  <-- The main fix for timezone issues
  };

  return dateObject.toLocaleDateString('en-IN', options);
};

export const getDateDifference = (dateString1, dateString2) => {
  const date1 = new Date(dateString1);
  const date2 = new Date(dateString2);

  // Calculate the difference in milliseconds
  const diffInMs = Math.abs(date2 - date1);

  // Convert milliseconds to days and get a whole number
  return Math.floor(diffInMs / (1000 * 60 * 60 * 24));
};

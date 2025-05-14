// src/api/serviceApi.js
export const getServices = async () => {
  // Simulasi delay
  await new Promise(resolve => setTimeout(resolve, 300));

  return [
    {
      id: 1,
      title: 'Classic Haircut',
      description: 'A timeless haircut for all occasions.',
      price: '$20',
      icon: 'scissors'
    },
    {
      id: 2,
      title: 'Modern Fade',
      description: 'Trendy fade haircut with sharp lines.',
      price: '$25',
      icon: 'fade'
    },
    {
      id: 3,
      title: 'Beard Trim',
      description: 'Professional beard shaping and trimming.',
      price: '$15',
      icon: 'beard'
    }
  ];
};

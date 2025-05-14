// src/api/bookingApi.js
export const submitBooking = async (bookingData) => {
  // Simulasi API call
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log('Booking submitted:', bookingData);
      resolve({ success: true, message: 'Booking successful' });
    }, 1000);
  });
};

// src/api/authApi.js
export const login = async (credentials) => {
  // Simulasi API call
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log('Login attempt:', credentials);
      resolve({ success: true, token: 'sample-token', user: { name: 'John Doe' } });
    }, 1000);
  });
};

// src/api/serviceApi.js
export const getServices = async () => {
  // Simulasi API call
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        {
          id: 1,
          title: 'Classic Haircut',
          description: 'Traditional haircut with clippers and scissors for a clean, classic look.',
          price: 'Rp 80.000',
          icon: 'scissors'
        },
        {
          id: 2,
          title: 'Beard Trim',
          description: 'Professional beard shaping and trimming to enhance your facial features.',
          price: 'Rp 50.000',
          icon: 'razor'
        },
        {
          id: 3,
          title: 'Hot Towel Shave',
          description: 'Luxurious straight razor shave with hot towel treatment for ultimate relaxation.',
          price: 'Rp 70.000',
          icon: 'towel'
        },
        {
          id: 4,
          title: 'Hair Coloring',
          description: 'Professional hair coloring service with premium products for vibrant results.',
          price: 'Rp 150.000',
          icon: 'color'
        },
        {
          id: 5,
          title: 'Kids Haircut',
          description: 'Gentle and patient haircut service for children under 12.',
          price: 'Rp 60.000',
          icon: 'kid'
        },
        {
          id: 6,
          title: 'Hair Treatment',
          description: 'Revitalizing hair treatments to restore shine and health to your hair.',
          price: 'Rp 120.000',
          icon: 'treatment'
        }
      ]);
    }, 500);
  });
};

// src/api/barberApi.js
export const getBarbers = async () => {
  // Simulasi delay 300ms untuk meniru fetch API
  await new Promise(resolve => setTimeout(resolve, 300));

  return [
    {
      id: 1,
      name: 'Federico Dimarco',
      position: 'Master Barber',
      image: '/assets/images/barber-1.jpeg',
      expertise: 'Classic cuts, Fades, Beard styling',
      experience: '8 years',
      social: {
        instagram: 'https://instagram.com/johndoe',
        facebook: '#',
        twitter: '#'
      }
    },
    {
      id: 2,
      name: 'Cornelia Vanisa',
      position: 'Style Expert',
      image: '/assets/images/barber-2.jpeg',
      expertise: 'Modern styles, Hair coloring, Skin fades',
      experience: '6 years',
      social: {
        instagram: 'https://instagram.com/mikesmith',
        facebook: '#',
        twitter: '#'
      }
    },
    {
      id: 3,
      name: 'Kang Mus',
      position: 'Senior Barber',
      image: '/assets/images/barber-3.jpeg',
      expertise: 'Textured cuts, Hair treatments, Beard designs',
      experience: '5 years',
      social: {
        instagram: 'https://instagram.com/davidwilson',
        facebook: '#',
        twitter: '#'
      }
    },
    {
      id: 4,
      name: 'Yasir A Fauzan',
      position: 'Junior Barber',
      image: '/assets/images/barber-4.jpeg',
      expertise: 'Classic cuts, Hot towel shaves, Hair styling',
      experience: '3 years',
      social: {
        instagram: 'https://instagram.com/robertjohnson',
        facebook: '#',
        twitter: '#'
      }
    },
        {
      id: 5,
      name: 'Bang Ale',
      position: 'Senior Barber',
      image: '/assets/images/barber-5.jpg',
      expertise: 'Classic cuts, Hot towel shaves, Hair styling',
      experience: '3 years',
      social: {
        instagram: 'https://instagram.com/robertjohnson',
        facebook: '#',
        twitter: '#'
      }
    }
  ];
};

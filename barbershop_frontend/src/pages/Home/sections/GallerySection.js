import React, { useState } from 'react';
import GalleryItem from '../../../components/GalleryItem/GalleryItem';

const GallerySection = () => {
  const galleryImages = [
    {
      id: 1,
      src: '/assets/images/haircut-1.jpg',
      alt: 'Classic Haircut',
      category: 'haircut'
    },
    {
      id: 2,
      src: '/assets/images/haircut-2.jpg',
      alt: 'Modern Fade',
      category: 'haircut'
    },
    {
      id: 3,
      src: '/assets/images/beard-1.jpg',
      alt: 'Beard Trim',
      category: 'beard'
    },
    {
      id: 4,
      src: '/assets/images/haircut-3.jpg',
      alt: 'Textured Crop',
      category: 'haircut'
    },
    {
      id: 5,
      src: '/assets/images/beard-2.jpg',
      alt: 'Full Beard Styling',
      category: 'beard'
    },
    {
      id: 6,
      src: '/assets/images/haircut-4.jpg',
      alt: 'Pompadour Style',
      category: 'haircut'
    },
    {
      id: 7,
      src: '/assets/images/color-1.jpg',
      alt: 'Hair Coloring',
      category: 'color'
    },
    {
      id: 8,
      src: '/assets/images/haircut-5.jpg',
      alt: 'Undercut Style',
      category: 'haircut'
    }
  ];

  const [filter, setFilter] = useState('all');

  const filteredImages = filter === 'all' 
    ? galleryImages 
    : galleryImages.filter(img => img.category === filter);

  return (
    <section id="gallery" className="gallery-section">
      <div className="container">
        <div className="section-header">
          <h2>Our Gallery</h2>
          <p>Check out our latest work and masterpieces</p>
        </div>
        
        <div className="gallery-filter">
          <button 
            className={filter === 'all' ? 'active' : ''} 
            onClick={() => setFilter('all')}
          >
            All
          </button>
          <button 
            className={filter === 'haircut' ? 'active' : ''} 
            onClick={() => setFilter('haircut')}
          >
            Haircuts
          </button>
          <button 
            className={filter === 'beard' ? 'active' : ''} 
            onClick={() => setFilter('beard')}
          >
            Beard
          </button>
          <button 
            className={filter === 'color' ? 'active' : ''} 
            onClick={() => setFilter('color')}
          >
            Coloring
          </button>
        </div>
        
        <div className="gallery-grid">
          {filteredImages.map(image => (
            <GalleryItem key={image.id} image={image} />
          ))}
        </div>
      </div>
    </section>
  );
};

export default GallerySection;

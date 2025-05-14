import React from 'react';
import BarberProfile from '../../../components/BarberProfile/BarberProfile';

const AboutSection = () => {
  const teamMembers = [
    {
      id: 1,
      name: 'John Doe',
      position: 'Master Barber',
      image: '/assets/images/barber-1.jpg',
      social: {
        instagram: '#',
        facebook: '#',
        twitter: '#'
      }
    },
    {
      id: 2,
      name: 'Mike Smith',
      position: 'Senior Barber',
      image: '/assets/images/barber-2.jpg',
      social: {
        instagram: '#',
        facebook: '#',
        twitter: '#'
      }
    },
    {
      id: 3,
      name: 'David Wilson',
      position: 'Style Expert',
      image: '/assets/images/barber-3.jpg',
      social: {
        instagram: '#',
        facebook: '#',
        twitter: '#'
      }
    },
    {
      id: 4,
      name: 'Robert Johnson',
      position: 'Junior Barber',
      image: '/assets/images/barber-4.jpg',
      social: {
        instagram: '#',
        facebook: '#',
        twitter: '#'
      }
    }
  ];

  return (
    <section id="about" className="about-section">
      <div className="container">
        <div className="section-header">
          <h2>About Us</h2>
          <p>Get to know our story and our team of professionals</p>
        </div>
        
        <div className="about-content">
          <div className="about-image">
            <img src="/assets/images/barbershop-interior.jpg" alt="Barbershop Interior" />
          </div>
          <div className="about-text">
            <h3>Our Story</h3>
            <p>
              Founded in 2015, BarberStyle has been providing premium haircuts and grooming services to men who appreciate quality and style. Our journey began with a simple mission: to create a space where men can enjoy exceptional grooming services in a relaxed and friendly atmosphere.
            </p>
            <p>
              What sets us apart is our commitment to precision, attention to detail, and personalized service. Each haircut is tailored to enhance your unique features and style preferences. Our barbers are not just skilled professionals; they are artists who take pride in their craft.
            </p>
            <p>
              At BarberStyle, we believe that a great haircut is more than just a service—it's an experience that boosts your confidence and leaves you looking and feeling your best.
            </p>
            <div className="about-stats">
              <div className="stat">
                <span className="stat-number">8+</span>
                <span className="stat-text">Years of Experience</span>
              </div>
              <div className="stat">
                <span className="stat-number">15k+</span>
                <span className="stat-text">Happy Clients</span>
              </div>
              <div className="stat">
                <span className="stat-number">4</span>
                <span className="stat-text">Expert Barbers</span>
              </div>
            </div>
          </div>
        </div>
        
        <div className="team-section">
          <h3>Meet Our Team</h3>
          <div className="team-grid">
            {teamMembers.map(member => (
              <BarberProfile key={member.id} barber={member} />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default AboutSection;
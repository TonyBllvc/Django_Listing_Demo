from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView 
from .models import Listing
from rest_framework import permissions, status
from rest_framework.response import Response
from django.contrib.postgres.search import SearchQuery, SearchVector
from .serializers import ListingSerializer, ListingUpdateSerializer

# Create your views here.
class ManageListingView(APIView):

    def get(self, request, format=None):
        try:
            
            user = request.user
            
            if not user.is_realtor: # verify user has permission
                return Response({"status": "error", "error": "User does not have necessary permission for this listing data"}, status=status.HTTP_403_FORBIDDEN) 
            
            slug = request.query_params.get('slug') # passing slug as a params 

            # ***** full data set for specific realtors ******
            # Get all Listings relating to a a particular realtor
            if not slug:
                listing = Listing.objects.order_by('-date_created').filter(realtor=user.email)

                listing = ListingSerializer(listing, many=True) # retrieves as a List
            
                return Response({"status": "success", "data": listing.data,}, status=status.HTTP_200_OK)
            
            # if no listing exists for the realtor 
            listing_exists =  Listing.objects.filter(realtor=user.email, slug=slug).exists() # retrieves as a List

            if not listing_exists:
                return Response({"status": "error", "error": "No listing exists"}, status=status.HTTP_404_NOT_FOUND)
            
            if listing_exists:
                # if it then exists for the particular realtor
                listing = Listing.objects.get(realtor=user.email, slug=slug) # Retrieves as a dictionary

                listing = ListingSerializer(listing) # Retrieves as a dictionary
            
                return Response({"status": "success", "data": listing.data,}, status=status.HTTP_200_OK)
            
            # all_listings_available = Listing.objects.all()

            # if not all_listings_available:
            #     return Response({"status": "error", "error": "No listing exists"}, status=status.HTTP_404_NOT_FOUND)

            # if all_listings_available:
                
            #     listing = ListingSerializer(all_listings_available) # Retrieves as a dictionary

            #     return Response({"status": "success", "data": listing.data,}, status=status.HTTP_200_OK)

        except:
            return Response({"status": "error", "error": "Something went wrong when creating listing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


    def retrieve_values(self, data):

            title = data['title']
            address = data['address']
            city = data['city']
            state = data['state']
            zipcode = data['zipcode']
            description = data['description']
            
            slug = data['slug']

            print('pan')
            print(slug)
            # list_slug_exist = get_object_or_404(Listing, slug=slug)
            # if list_slug_exist:
            #     return Response({"status": "error", "error": "Listing with this slug already exists"}, status=status.HTTP_400_BAD_REQUEST)

            # # Validate required fields
            if not all([title, address, city, state, zipcode, description]):
                return Response({"status": "error", "error": "Please fill in all the required fields"}, status=status.HTTP_400_BAD_REQUEST)
            
            print('low')
            price = data['price']
            bedrooms = data['bedrooms']
            bathrooms = data['bathrooms']
            sale_type = data['sale_type']
            
            # # Validate required fields
            if not all([price, bedrooms, bathrooms, sale_type]):
                return Response({"status": "error", "error": "Please fill in all the required fields"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                price = int(price)
            except:
                return Response({"status": "error", "error": "Make an integer"}, status=status.HTTP_400_BAD_REQUEST)

            print('low one')
            try:
                bedrooms = int(bedrooms)
            except:
                return Response({"status": "error", "error": "Make an integer"}, status=status.HTTP_400_BAD_REQUEST)
            
            print('low two')
            try:
                bathrooms = float(bathrooms)
            except:
                return Response({"status": "error", "error": "Make an integer"}, status=status.HTTP_400_BAD_REQUEST)
            
            if bathrooms <= 0 or bathrooms >= 10:
                bathrooms = 1.0

            bathrooms = round(bathrooms, 1)

            print('where')
            
            if sale_type == 'FOR_RENT':
                sale_type = 'For Rent'
            elif sale_type == 'FOR_SALE':
                sale_type = 'For Sale'
            else: 
                return Response({"status": "error", "error": "Pick a sales type"}, status=status.HTTP_400_BAD_REQUEST)


            print('where pl')
            home_type = data['home_type']
            
            # print(home_type)
            if home_type == 'CONDO':
                home_type = 'Condo'
            elif home_type == 'HOUSE':
                home_type = 'House'
            elif home_type == 'TOWNHOUSE':
                home_type = 'Townhouse'
            else: 
                return Response({"status": "error", "error": "Pick a home type"}, status=status.HTTP_400_BAD_REQUEST)
            
            print('where as')
            # sale_type = data['sale_type']
            # if sale_type not in ['FOR_SALE', 'FOR_RENT']:
            #     return Response({"status": "error", "error": "Invalid sale type"}, status=status.HTTP_400_BAD_REQUEST)
            # sale_type = 'For Rent' if sale_type == 'FOR_RENT' else 'For Sale'

            # home_type = data['home_type']
            # if home_type not in ['CONDO', 'HOUSE', 'TOWNHOUSE']:
            #     return Response({"status": "error", "error": "Invalid home type"}, status=status.HTTP_400_BAD_REQUEST)
            # home_type = home_type.capitalize()

            # if not 
            main_photo = data['main_photo']
            photo_1 = data['photo_1']
            photo_2 = data['photo_2']
            photo_3 = data['photo_3']
            is_published = data['is_published']

            # # Validate required fields
            if not all([main_photo, photo_1, photo_2, photo_3, is_published]):
                return Response({"status": "error", "error": "Please fill in all the required fields"}, status=status.HTTP_400_BAD_REQUEST)
            

            print('how')
            print(main_photo)
            if is_published == 'True':
                is_published = True
            else:
                is_published = False
            
            print('yam')

            print(f'slug: {slug}')
            
            data =  {
                'title': title,
                'slug': slug,
                'address': address,
                'city': city,
                'state': state,
                'zipcode': zipcode,
                'description': description,
                'price': price,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'sale_type': sale_type,
                'home_type': home_type,
                'main_photo': main_photo,
                'photo_1': photo_1,
                'photo_2': photo_2,
                'photo_3': photo_3,
                'is_published': is_published

            }

            print('success')
            return data
    

    def post(self, request):
        print('ran')
        try:
            print('okay')
            user = request.user

            if not user.is_realtor:
                return Response({"status": "error", "error": "User does not have necessary permission for creating this listing data"}, status=status.HTTP_403_FORBIDDEN) 
            
            data = request.data

            data = self.retrieve_values(data)

            title  = data['title']
            slug = data['slug']
            address = data['address']
            city = data['city']
            state = data['state']
            zipcode = data['zipcode']
            description = data['description']
            price  = data['price']
            bedrooms = data['bedrooms']
            bathrooms = data['bathrooms']
            sale_type = data['sale_type']
            home_type = data['home_type']
            main_photo = data['main_photo']
            photo_1 = data['photo_1']
            photo_2 = data['photo_2']
            photo_3 = data['photo_3']
            is_published = data['is_published']

            if Listing.objects.filter(slug=slug).exists():
                return Response({"status": "error", "error": "Listing with this slug already exists"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                print('okay nah')
                listing = Listing.objects.create(
                    realtor=user.email,
                    title=title,
                    slug=slug,
                    address=address,
                    city=city,
                    state=state,
                    zipcode=zipcode,
                    description=description,
                    price=price,
                    bedrooms=bedrooms,
                    bathrooms=bathrooms,
                    sale_type=sale_type,
                    home_type=home_type,
                    main_photo=main_photo,
                    photo_1=photo_1,
                    photo_2=photo_2,
                    photo_3=photo_3,
                    is_published=is_published
                )

                serializer = ListingSerializer(listing)
                print('okay lap')
                return Response({"status": "success", "data": serializer.data, "message": "Listing created successfully"}, status=status.HTTP_201_CREATED)
            # # Validate required fields
            # if not all([title, slug, address, city, state, zipcode, description, bedrooms, bathrooms, main_photo]):
            #     return Response({"status": "error", "error": "Please fill in all the required fields"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"status": "error", "error": f"Error creating listing: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      

        except:
            return Response({"status": "error", "error": "Something went wrong when creating listing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

    def put(self, request):
        try:
            
            user = request.user

            if not user.is_realtor:
                return Response({"status": "error", "error": "User does not have necessary permission for updating this listing data"}, status=status.HTTP_403_FORBIDDEN) 
            
            data = request.data

            print('okay nah me')
            data = self.retrieve_values(data)

            print('okay nah u')
            title  = data['title']
            slug = data['slug']
            address = data['address']
            city = data['city']
            state = data['state']
            zipcode = data['zipcode']
            description = data['description']
            price  = data['price']
            bedrooms = data['bedrooms']
            bathrooms = data['bathrooms']
            sale_type = data['sale_type']
            home_type = data['home_type']
            main_photo = data['main_photo']
            photo_1 = data['photo_1']
            photo_2 = data['photo_2']
            photo_3 = data['photo_3']
            is_published = data['is_published']

            print('okay nah p')

            # print(f'slug: {slug}')

            # print(f'me: {user.email}')
            
            if not Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response({"status": "error", "error": "Non-existent listing"}, status=status.HTTP_404_NOT_FOUND) 
            
            print('okay nah q')       
            # try:     
            Listing.objects.filter(realtor=user.email, slug=slug).update(
                title=title,
                slug=slug,
                address=address,
                city=city,
                state=state,
                zipcode=zipcode,
                description=description,
                price=price,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                sale_type=sale_type,
                home_type=home_type,
                main_photo=main_photo,
                photo_1=photo_1,
                photo_2=photo_2,
                photo_3=photo_3,
                is_published=is_published
            )

            # Retrieve the updated listing object
            updated_listing = Listing.objects.get(realtor=user.email, slug=slug)
            serializer = ListingUpdateSerializer(updated_listing)
            print('printed')
            return Response({"status": "success", "data": serializer.data, "message": "Listing updated successfully"}, status=status.HTTP_200_OK)
        
        except Exception as e:
                return Response({"status": "error", "error": f"Error creating listing: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            return Response({"status": "error", "error": "Something went wrong when updating listing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        

    def patch(self, request):
        try:
            user = request.user

            if not user.is_realtor:
                return Response({"status": "error", "error": "User does not have necessary permission for updating this listing data"}, status=status.HTTP_403_FORBIDDEN) 
            
            data = request.data

            slug = data['slug']

            is_published = data['is_published']

            if is_published == 'True':
                is_published = True
            else:
                is_published = False
            
            if not Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response({"status": "error", "error": "Non-existent listing"}, status=status.HTTP_404_NOT_FOUND) 
            
            Listing.objects.filter(realtor=user.email, slug=slug).update(
                is_published=is_published
            )

            # Retrieve the updated listing object
            updated_listing = Listing.objects.get(realtor=user.email, slug=slug)

            serializer = ListingSerializer(updated_listing)
            print('printed')
            return Response({"status": "success", "data": serializer.data, "message": "Listing updated successfully"}, status=status.HTTP_200_OK)
        
        
        except Exception as e:
                return Response({"status": "error", "error": f"Error creating listing: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            return Response({"status": "error", "error": "Something went wrong when updating listing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        

    def delete(self, request):
        try:
            user = request.user

            if not user.is_realtor:
                return Response({"status": "error", "error": "User does not have necessary permission for updating this listing data"}, status=status.HTTP_403_FORBIDDEN) 
            
            data = request.data

            slug = data['slug']
  
            if not Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response({"status": "error", "error": "Non-existent listing"}, status=status.HTTP_404_NOT_FOUND) 
            
            # Retrieve the updated listing object
            updated_listing = Listing.objects.get(realtor=user.email, slug=slug)


            serializer = ListingSerializer(updated_listing)

            print('printed')

            updated_listing.delete()
            # Listing.objects.filter(realtor=user.email, slug=slug).delete()
            
            if not Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response({"status": "success", "data": serializer.data, "message": "Listing deleted successfully"}, status=status.HTTP_204_NO_CONTENT) 
            else:
                return Response({"status": "success", "message": "Failed to delete listing"}, status=status.HTTP_400_BAD_REQUEST)

            # return Response({"status": "success", "data": serializer.data, "message": "Listing updated successfully"}, status=status.HTTP_200_OK)
        
        

        except Exception as e:
                return Response({"status": "error", "error": f"Error creating listing: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            return Response({"status": "error", "error": "Something went wrong when updating listing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
        

class ListingDetailView(APIView):
    def get(self, request, format=None):
        try:
            slug = request.query_params.get('slug') # passing slug as a params 
            
            if not slug:
                return Response({"status": "error", "error": "No slug passed"}, status=status.HTTP_400_BAD_REQUEST)
            
            # slug_exists = Listing.objects.filter(slug=slug).exists()

            slug_published = Listing.objects.filter(slug=slug, is_published=True).exists()

            # if not slug_exists:
            #     return Response({"status": "error", "error": "Listing does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            if not slug_published:
                return Response({"status": "error", "error": "No published listings found"}, status=status.HTTP_404_NOT_FOUND)
            
            listing_exists = Listing.objects.get(slug=slug, is_published=True)

            listing_exists = ListingSerializer(listing_exists)

            return Response({"status": "success", "data": listing_exists.data, }, status=status.HTTP_200_OK)
      
        except:
            return Response({"status": "error", "error": "Something went wrong when retrieving detail"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

class ListingsView(APIView):
    permission_classes = [permissions.AllowAny] # I do not need to be authenticated
    
    def get(self, request, format=False):
        try:
            published = Listing.objects.filter(is_published=True).exists()
        
            if not published:
                return Response({"status": "error", "error": "No published listings found"}, status=status.HTTP_404_NOT_FOUND)
            
            published_list = Listing.objects.order_by('-date_created').filter(is_published=True)

            published_list = ListingSerializer(published_list, many=True) # a list

            return Response({"status": "success", "data": published_list.data}, status=status.HTTP_200_OK)

        except:
            return Response({"status": "error", "error": "Something went wrong when retrieving listing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


# Note: Every commentation there is useful
class SearchListingsView(APIView):
    permission_classes = [permissions.AllowAny] # I do not need to be authenticated

    def get(self, request, format=None):
        try:

            search = request.query_params.get('search')

            if search:
                # Assuming you need to search through  ('title' OR 'description') AND 'is_published' fields

                listings = Listing.objects.annotate(
                    search=SearchVector('title', 'description')
                ).filter(search=SearchQuery(search), is_published=True)

                # Still works as a normal get.
                # listing_get = Listing.objects.get(title__search=search)
                
                if listings.exists():

                     #  Now in this example, I am searching through ('title' OR 'description') fields AND 'description'..

                     # or 

                     #  .. Whereas I am only searching through 'title' AND 'description'  fields

                     # Assuming you need to search through  'title' AND 'is_published' fields
                     # *** [ Must be a complete word in conjunction to the existing dataset in the field]
                     # listings = Listing.objects.filter(
                     #     title__search=search, # for searching through for specific word  
                     #     is_published=True
                     # )

                     # For a bigger project, query just the typed
                     # *** [ Must not be a compete word in conjunction to the existing dataset in the field] **
                     #  can be just a letter
                     # if search:
                     #     listings = Listing.objects.filter(title__icontains=search) # to scan for query
                     # else:
                     #     listings = Listing.objects.all()


                     print(f'listings: {listings}')
                    #  print(f'listing get: {listing_get}')

                     print(type(listings))
                    #  print(type(listing_get))

                     for listing in listings:
                         print(f'listing: {listing.title}')

                     return Response({"status": "success", "data": 'search went ok'}, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "error", "error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

            elif not search:
                listing = Listing.objects.all()

                return Response({"status": "success", "data": 'search went okay'}, status=status.HTTP_200_OK)

        except Exception as e:
                return Response({"status": "error", "error": f"Error creating listing: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            return Response({"status": "error", "error": "Something went wrong when updating listing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
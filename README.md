# Api parser faust
### About
This app parsing products by category from 2 fake store api:
- https://dummyjson.com/
- https://fakestoreapi.com/
**Valid categories:**
- jewelery
- electronics
- men-clothing
- woman-clothing
### Installation:
1. create folder where you want expand project and go there 
2. write a command: git clone https://github.com/emilrakaev/api_parser_faust/
3. write a command: docker-compose build
4. write a command: docker-compose up
### Endpoints documentation
- **Search by category**
   - Path: http://macbook-pro-emil.local:6066/search/?q={category}
   - Method: GET
   - Response: {"uuid":"b7c8aaa1-b6be-4751-a7e8-bba2ca7d3c75"}
 - **Get results by uuid**
   - Path: http://macbook-pro-emil.local:6066/result/?q={uuid}
   - Method: GET
   - Response: {"results":[{"title":"Silver Ring Set Women","price":70},{"title":"Rose Ring","price":100}]
### Run app
- run command: python3 -m parser_app worker -l info

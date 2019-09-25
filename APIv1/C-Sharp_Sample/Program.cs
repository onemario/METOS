using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Security.Cryptography;
using System.Text;
using System.Threading;
using System.Threading.Tasks;


namespace Demo.Metos.API
{
    internal class Program
    {
        /// <summary>
        /// Just executes the async function and waits until ready
        /// </summary>
        /// <param name="args"></param>
        private static void Main(string[] args)
        {
            RunAsync().Wait();
        }

        /// <summary>
        /// The asynchronous function prepares the HTTP client hander, 
        /// calls the API and processes the response.
        /// </summary>
        /// <returns>Task</returns>
        private static async Task RunAsync()
        {
            var httpHandler = new MetosHttpHandler(new HttpClientHandler());
            httpHandler.PublicKey = "ENTER YOUR public HMAC key";
            httpHandler.PrivateKey = "ENTER YOUR private HMAC key";

            Debug.Assert(httpHandler.PublicKey.StartsWith("ENTER") == false, "Please enter your public HMAC key!");
            Debug.Assert(httpHandler.PrivateKey.StartsWith("ENTER") == false, "Please enter your private HMAC key!");

            var httpClient = new HttpClient(httpHandler) { BaseAddress = httpHandler.ApiUri };
            httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
            
            var response = await httpClient.GetAsync("/user/stations");
 
            Console.WriteLine("Status {0}:{1} \n", response.StatusCode, await response.Content.ReadAsStringAsync());
        }
    }

    /// <summary>
    /// Custom HTTP handler with required setters
    /// </summary>
    public class MetosHttpHandler : DelegatingHandler
    {
        private static readonly CultureInfo _enUsCulture = new CultureInfo("en-us");
        private static readonly Uri _apiBaseAddress = new Uri("https://api.fieldclimate.com/v2");

        /// <summary>
        /// FieldClimate account: public HMAC key to access METOS station data and services 
        /// </summary>
        public string PublicKey { get; set; }

        /// <summary>
        /// FieldClimate account: private HMAC key to access METOS station data and services 
        /// </summary>
        public string PrivateKey { get; set; }

        /// <summary>
        /// Defaults to https://api.fieldclimate.com/v2
        /// </summary>
        public Uri ApiUri { get; set; }

        /// <summary>
        /// Default initialization
        /// </summary>
        /// <param name="handler"></param>
        public MetosHttpHandler(HttpMessageHandler handler)
        {
            base.InnerHandler = handler;
            ApiUri = _apiBaseAddress;
        }

        /// <summary>
        /// Provides custom HTTP header modification
        /// </summary>
        /// <param name="request"></param>
        /// <param name="cancellationToken"></param>
        /// <returns></returns>
        protected override async Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
        {
            HttpResponseMessage response = null;

            // recover missing version part (e.g. /v1)
            var requestRoute = request.RequestUri.AbsolutePath;
            string combinedPath = ApiUri.AbsolutePath + requestRoute;
            request.RequestUri = new Uri(ApiUri, combinedPath);
            // adjust HTTP authorization header
            var requestHttpMethod = request.Method.Method;
            var date = DateTimeOffset.UtcNow;
            request.Headers.Date = date;
            var requestTimeStamp = date.ToString("ddd, dd MMM yyyy HH:mm:ss 'GMT'", _enUsCulture);
            var signatureRawData = $"{requestHttpMethod}{requestRoute}{requestTimeStamp}{PublicKey}";
            var privateKeyByteArray = Encoding.UTF8.GetBytes(PrivateKey);
            var signature = Encoding.UTF8.GetBytes(signatureRawData);
            using (var hmac = new HMACSHA256(privateKeyByteArray))
            {
                var signatureBytes = hmac.ComputeHash(signature);
                var requestSignatureString = ByteArrayToString(signatureBytes);
                request.Headers.Authorization = new AuthenticationHeaderValue("hmac",
                    $"{PublicKey}:{requestSignatureString}");
            }

            response = await base.SendAsync(request, cancellationToken);
            return response;
        }

        /// <summary>
        /// Helper function to produce a hex string
        /// </summary>
        /// <param name="ba"></param>
        /// <returns></returns>
        private static string ByteArrayToString(IReadOnlyCollection<byte> ba)
        {
            var hex = new StringBuilder(ba.Count * 2);
            foreach (var b in ba)
                hex.AppendFormat("{0:x2}", b);
            return hex.ToString();
        }
    }
}
